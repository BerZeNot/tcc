#!/bin/bash

# Encontra e mata processos do main.py
pkill -f "python.*main.py"

# Aguarda um momento para garantir que o processo foi encerrado
sleep 0.5

# Inicia a aplicação
source .venv/bin/activate
python main.py
