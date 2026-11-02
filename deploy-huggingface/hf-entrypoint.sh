#!/bin/bash
# Entrypoint do CTFd para Hugging Face Spaces.
#
# Persistência: um Storage Bucket montado em /data.
#  - SQLite não funciona bem direto sobre um bucket (armazenamento de objetos),
#    então o banco roda no disco local do Space e um snapshot consistente é
#    copiado para /data/ctfd.db a cada 30 s e ao desligar. Na partida, ele é restaurado.
#  - Uploads (anexos, imagens) são gravados direto em /data/uploads.
# Sem /data, tudo é efêmero (some ao reiniciar).
set -uo pipefail

LOCAL=/tmp/ctfd
mkdir -p "$LOCAL/logs"
PERSIST=""

if [ -d /data ] && [ -w /data ]; then
    PERSIST=/data
    mkdir -p /data/uploads
    if [ -f /data/ctfd.db ]; then
        cp /data/ctfd.db "$LOCAL/ctfd.db"
        echo "[ HF ] Banco restaurado de /data/ctfd.db"
    else
        echo "[ HF ] Nenhum banco salvo ainda em /data (primeira execução)"
    fi
    UPLOADS=/data/uploads
else
    echo "[ AVISO ] /data indisponível: banco e uploads são EFÊMEROS (somem ao reiniciar)."
    UPLOADS="$LOCAL/uploads"
    mkdir -p "$UPLOADS"
fi

export DATABASE_URL="sqlite:///$LOCAL/ctfd.db"
export UPLOAD_FOLDER="$UPLOADS"
export LOG_FOLDER="$LOCAL/logs"

snapshot() {
    [ -n "$PERSIST" ] && [ -f "$LOCAL/ctfd.db" ] || return 0
    python - "$LOCAL/ctfd.db" "$LOCAL/snapshot.db" "$PERSIST/ctfd.db" <<'PY'
import hashlib, os, shutil, sqlite3, sys
src, tmp, dst = sys.argv[1:4]
if os.path.exists(tmp):
    os.remove(tmp)
origem = sqlite3.connect(src)
destino = sqlite3.connect(tmp)
origem.backup(destino)          # cópia consistente, mesmo com o CTFd escrevendo
destino.close(); origem.close()
novo = hashlib.sha256(open(tmp, "rb").read()).hexdigest()
marca = tmp + ".sha256"
antigo = open(marca).read() if os.path.exists(marca) else ""
if novo != antigo:
    shutil.copyfile(tmp, dst)
    open(marca, "w").write(novo)
PY
}

if [ -n "$PERSIST" ]; then
    ( while sleep 30; do snapshot || echo "[ HF ] falha no snapshot"; done ) &
    LOOP=$!
fi

cd /opt/CTFd
./docker-entrypoint.sh &
CTFD=$!

encerrar() {
    echo "[ HF ] Encerrando: salvando snapshot final"
    snapshot
    kill -TERM "$CTFD" 2>/dev/null
    wait "$CTFD"
    exit 0
}
trap encerrar TERM INT

wait "$CTFD"
STATUS=$?
snapshot
[ -n "${LOOP:-}" ] && kill "$LOOP" 2>/dev/null
exit $STATUS
