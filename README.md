# Monk the Monkey

Este é um jogo de plataforma desenvolvido em Python utilizando a biblioteca **Pygame**. O projeto inclui mapas, efeitos sonoros, música de fundo e diversas mecânicas de jogabilidade.

---

## Pré-requisitos

Antes de executar o jogo, certifique-se de que você tenha os seguintes requisitos instalados:

 **Biblioteca Pygame**
   - Instale usando o seguinte comando:
     ```bash
     pip install pygame
     ```

---

## Estrutura do Projeto

```plaintext
📂 projeto-raiz/
├── 📁 data/                   # Recursos do jogo
│   ├── 📁 images/             # Sprites e imagens
│   ├── 📁 maps/               # Arquivos JSON com os mapas do jogo
│   ├── 📁 sfx/                # Efeitos sonoros e música
│       ├── ambience.wav       # Som ambiente
│       ├── dash.wav           # Som do dash
│       ├── hit.wav            # Som de impacto
│       ├── jump.wav           # Som do pulo
│       ├── shoot.wav          # Som do tiro
│       ├── music.wav          # Música de fundo
├── 📁 src/                    # Código-fonte do jogo
│   ├── clouds.py              # Lógica de nuvens
│   ├── entities.py            # Lógica de jogadores e inimigos
│   ├── map_editor.py          # Editor de mapas
│   ├── menu.py                # Lógica do menu principal
│   ├── particle.py            # Efeitos de partículas
│   ├── tilemap.py             # Manipulação de mapas e tiles
│   ├── util.py                # Funções utilitárias
│   ├── game.py                # Arquivo principal do jogo
├── README.md                  # Documentação do projeto
└── map_json/                  # Mapas prontos para uso

```


## Como Rodar o Jogo

1. **Clone ou baixe este repositório**
   - Clone usando o Git:
     ```bash
     git clone https://github.com/seu-repositorio/jogo-plataforma.git
     ```
   - Ou baixe como um arquivo ZIP e extraia.

2. **Acesse o diretório do projeto**
   ```bash
   cd jogo-plataforma/src
   ```

3. **Rode o jogo**
    ```bash
    python game.py
    ```
