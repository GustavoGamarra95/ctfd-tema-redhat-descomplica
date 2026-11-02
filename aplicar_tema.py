"""Aplica o tema "CTF Red Hat + Descomplica UniAmérica" a uma instância do CTFd.

O que faz (via API, com um token de admin):
  1. Envia assets/cyber_skyline.svg como arquivo de página.
  2. Grava o nome do CTF, a descrição e o Theme Header (CSS), apontando o
     fundo da cidade para o arquivo enviado.
  3. Substitui a página inicial (rota "index") por index.html.

Uso:
  CTFD_TOKEN=ctfd_... python aplicar_tema.py https://meu-ctfd.exemplo

Só usa a biblioteca padrão do Python.
"""

import json
import os
import sys
import urllib.request
import uuid
from pathlib import Path

AQUI = Path(__file__).resolve().parent
NOME = "CTF Red Hat + Descomplica UniAmérica"
DESCRICAO = "Capture The Flag — Red Hat Brasil + Descomplica UniAmérica · 06/11 19:00"


def requisicao(base: str, token: str, metodo: str, caminho: str, corpo=None,
               tipo="application/json"):
    dados = json.dumps(corpo).encode() if tipo == "application/json" and corpo is not None else corpo
    req = urllib.request.Request(base + caminho, data=dados, method=metodo, headers={
        "Authorization": f"Token {token}",
        "Content-Type": tipo,
    })
    with urllib.request.urlopen(req) as resp:
        resposta = json.load(resp)
    if not resposta.get("success"):
        raise SystemExit(f"Falhou em {metodo} {caminho}: {resposta}")
    return resposta


def enviar_arquivo(base: str, token: str, arquivo: Path) -> str:
    fronteira = uuid.uuid4().hex
    partes = [
        f"--{fronteira}\r\nContent-Disposition: form-data; name=\"type\"\r\n\r\npage\r\n".encode(),
        (f"--{fronteira}\r\nContent-Disposition: form-data; name=\"file\"; "
         f"filename=\"{arquivo.name}\"\r\nContent-Type: image/svg+xml\r\n\r\n").encode(),
        arquivo.read_bytes(),
        f"\r\n--{fronteira}--\r\n".encode(),
    ]
    resposta = requisicao(base, token, "POST", "/api/v1/files", b"".join(partes),
                          tipo=f"multipart/form-data; boundary={fronteira}")
    return resposta["data"][0]["location"]


def main() -> None:
    if len(sys.argv) != 2 or not os.environ.get("CTFD_TOKEN"):
        raise SystemExit(__doc__)
    base, token = sys.argv[1].rstrip("/"), os.environ["CTFD_TOKEN"]

    local = enviar_arquivo(base, token, AQUI / "assets" / "cyber_skyline.svg")
    print(f"[+] Cidade enviada: /files/{local}")

    tema = (AQUI / "theme_header.html").read_text().replace("__SKYLINE_URL__", f"/files/{local}")
    requisicao(base, token, "PATCH", "/api/v1/configs", {
        "ctf_name": NOME,
        "ctf_description": DESCRICAO,
        "theme_header": tema,
    })
    print("[+] Nome, descrição e Theme Header aplicados")

    paginas = requisicao(base, token, "GET", "/api/v1/pages")["data"]
    index = next((p for p in paginas if p["route"] == "index"), None)
    pagina = {
        "title": NOME, "route": "index", "format": "html",
        "content": (AQUI / "index.html").read_text(),
        "draft": False, "hidden": False, "auth_required": False,
    }
    if index:
        requisicao(base, token, "PATCH", f"/api/v1/pages/{index['id']}", pagina)
    else:
        requisicao(base, token, "POST", "/api/v1/pages", pagina)
    print("[+] Página inicial aplicada")


if __name__ == "__main__":
    main()
