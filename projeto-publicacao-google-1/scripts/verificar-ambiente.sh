#!/bin/bash

# Verificar se as variáveis de ambiente necessárias estão definidas
REQUIRED_VARS=("VAR1" "VAR2" "VAR3")  # Substitua VAR1, VAR2, VAR3 pelos nomes reais das variáveis

for VAR in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!VAR}" ]; then
        echo "Erro: A variável de ambiente $VAR não está definida."
        exit 1
    fi
done

echo "Todas as variáveis de ambiente necessárias estão definidas."