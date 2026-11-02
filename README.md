# Tema CTFd · CTF Red Hat + Descomplica UniAmérica

Tema visual do Capture The Flag **Red Hat Brasil + Descomplica UniAmérica**
(06/11, 19:00) para o [CTFd](https://ctfd.io) 3.8, aplicado sobre o tema `core`
sem modificar o código do CTFd.

- Paleta: vermelho Red Hat `#EE0000`, verde Descomplica `#00E88F`, preto.
- Fontes: Red Hat Display e Red Hat Mono (Google Fonts).
- Fundo cyberpunk: céu com névoa neon, cidade com janelas acesas, horizonte
  vermelho com faixa desfocada, grade em perspectiva animada, scanlines e
  faixas de glitch. As animações respeitam `prefers-reduced-motion`.
- Home com a bandeira + "CTF", logos Red Hat e Descomplica + UniAmérica,
  data e cursos.

## Arquivos

| Arquivo | O que é |
|---|---|
| `theme_header.html` | CSS + fontes, vai em **Admin → Config → Theme → Theme Header** (`__SKYLINE_URL__` é trocado pelo script) |
| `index.html` | Conteúdo da página inicial (rota `index`, formato HTML) |
| `assets/cyber_skyline.svg` | Silhueta da cidade do fundo (grande demais para ir dentro do Theme Header) |
| `assets/redhat.svg`, `assets/descomplica.svg` | Logos de referência (já embutidos no `index.html`) |
| `aplicar_tema.py` | Aplica tudo numa instância via API |
| `gerar_cidade.py` | Regenera `cyber_skyline.svg` (semente fixa, sai idêntico) |
| `deploy-huggingface/` | Dockerfile e entrypoint do Space do CTFd (persistência via Storage Bucket em `/data`) |

## Aplicar numa instância

1. Entre como admin e gere um token em **Settings → Access Tokens**.
2. Rode:

   ```bash
   CTFD_TOKEN=ctfd_... python aplicar_tema.py https://seu-ctfd.exemplo
   ```

O script envia a cidade como arquivo de página, grava nome, descrição e
Theme Header, e substitui a página inicial. Só usa a biblioteca padrão.

Para desfazer: esvazie o Theme Header e edite a página `index` em **Admin → Pages**.

As marcas Red Hat e Descomplica pertencem aos seus donos; os logos estão aqui
apenas para o evento.
