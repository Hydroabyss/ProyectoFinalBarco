#!/bin/bash

# Instalar dependências do projeto
if [ -f package.json ]; then
    echo "Instalando dependências com npm..."
    npm install
else
    echo "Arquivo package.json não encontrado. Certifique-se de estar no diretório correto."
    exit 1
fi

echo "Dependências instaladas com sucesso."