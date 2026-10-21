# Sistema de Análise de Imagens de Espermatozoides

Este repositório contém o código fonte do trabalho de conclusão de curso **"Migração de
Sistema de Análise de Imagens de Espermatozoides para a Linguagem Python"** desenvolvido pelo aluno Paulo, do curso de Sistemas de Informação da Universidade Federal de Uberlândia.


## Pré-requisitos

- Ter o Python 3.14 ou superior instalado
- Ter o Pip3 instalado
- Criar um ambiente virtual com o Python Venv e ativá-lo no terminal

```SHELL 
# Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python3 -m venv .venv
.venv\Scripts\activate.bat
```
- Instalar as dependências do projeto

```SHELL
# Linux e Windows
pip3 install -r requirements.txt
```
Também é possível executar o programa com o script [run.sh](run.sh) (⚠️**apenas em linux***), que se encontra na 
raiz do projeto. Ele foi criado para ser executado a partir de um atalho do VSCode e 
executa três quatro: mata qualquer processo antigo do sistema, aguarda 0.5 segundo, 
ativa o ambiente virtual (*venv*) e executa o programa com o comando `python3 main.py`.

## Como Executar
Considerando que os pré-requisitos foram atendidos, para executar o programa,
basta utilizar o comando:

```SHELL
# Linux e Windows
python3 main.py
```

## Árvore de Diretórios do Projeto

```
.
├── app
│   ├── controller.py
│   ├── image_processor.py
│   └── __init__.py
├── app_prototype.spec
├── build.sh
├── config
│   ├── __init__.py
│   └── settings.py
├── lib
│   ├── bull_erode_dilate.py
│   ├── bull_semiagr_measurements.py
│   ├── bull_sep_heads.py
│   ├── calc_dist_point_line_no_abs.py
│   ├── cleancc.py
│   ├── clean_connected_components.py
│   ├── clear_border_coords.py
│   ├── clear_border.py
│   ├── drawline.py
│   ├── draw_pca_vectors.py
│   ├── entropy.py
│   ├── fftderiv.py
│   ├── follow.py
│   ├── gallus_segment.py
│   ├── gallus_sep_heads.py
│   ├── getbb.py
│   ├── get_extremities.py
│   ├── get_mountains.py
│   ├── get_zeros.py
│   ├── image.py
│   ├── mirror_im.py
│   ├── PCAxy.py
│   ├── perim.py
│   └── Symmetry.py
├── main.py
├── README.md
├── requirements.txt
├── run.sh
├── ui
│   ├── __init__.py
│   ├── main_window.py
│   └── views
│       ├── assets
│       │   ├── green-circle-check-big.svg
│       │   ├── green-play.svg
│       │   ├── plus.svg
│       │   ├── red-x.svg
│       │   └── yellow-folder.svg
│       ├── index.css
│       ├── index.html
│       └── index.js
└── utils
    └── file_utils.py
```