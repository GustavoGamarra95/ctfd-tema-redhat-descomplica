"""Gera assets/cyber_skyline.svg: a silhueta da cidade do fundo cyberpunk.

Duas camadas de prédios (fundo mais claro, frente mais escura), janelas acesas
em vermelho Red Hat, verde Descomplica e branco, antenas com luz vermelha e
alguns letreiros de neon. A semente fixa reproduz sempre a mesma cidade.

Uso:  python gerar_cidade.py
"""

import random
from pathlib import Path

LARGURA, ALTURA = 1600, 320
CAMADAS = [
    # cor, altura mín/máx, largura mín/máx, densidade de janelas
    ("#16161a", 60, 200, 40, 90, .25),
    ("#0d0d10", 90, 300, 30, 80, .55),
]


def gerar(semente: int = 7) -> str:
    rng = random.Random(semente)
    partes = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LARGURA} {ALTURA}" '
              'preserveAspectRatio="xMidYMax slice">']
    for camada, (cor, hmin, hmax, wmin, wmax, janelas) in enumerate(CAMADAS):
        x = -20
        while x < LARGURA:
            w, h = rng.randint(wmin, wmax), rng.randint(hmin, hmax)
            y = ALTURA - h
            partes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{cor}"/>')
            if rng.random() < .35:  # antena
                ax = x + w // 2
                partes.append(f'<rect x="{ax}" y="{y - rng.randint(10, 40)}" width="2" '
                              f'height="40" fill="{cor}"/>')
                if camada == 1:
                    partes.append(f'<circle cx="{ax + 1}" cy="{y - 30}" r="2.2" fill="#ee0000"/>')
            for wy in range(y + 8, ALTURA - 6, 10):
                for wx in range(x + 5, x + w - 6, 8):
                    if rng.random() < janelas * 0.35:
                        c = rng.choice(["#ee0000", "#00e88f", "#ffffff", "#00e88f"])
                        o = rng.choice([".35", ".55", ".8"])
                        partes.append(f'<rect x="{wx}" y="{wy}" width="3" height="4" '
                                      f'fill="{c}" opacity="{o}"/>')
            if camada == 1 and rng.random() < .18 and h > 140:  # letreiro de neon
                c = rng.choice(["#ee0000", "#00e88f"])
                partes.append(f'<rect x="{x + 4}" y="{y + 16}" width="4" '
                              f'height="{min(70, h - 30)}" fill="{c}" opacity=".9"/>')
            x += w + rng.randint(0, 6)
    partes.append("</svg>")
    return "".join(partes)


if __name__ == "__main__":
    destino = Path(__file__).resolve().parent / "assets" / "cyber_skyline.svg"
    destino.write_text(gerar())
    print(f"[+] {destino} ({destino.stat().st_size} bytes)")
