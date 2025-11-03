# Projeto de Publicação no Google

Este projeto tem como objetivo facilitar a publicação de aplicações no Google. Abaixo estão as instruções para instalação e uso.

## Estrutura do Projeto

```
projeto-publicacao-google
├── .vscode
│   └── tasks.json          # Configuração das tarefas do VS Code
├── scripts
│   ├── instalar-dependencias.sh  # Script para instalar dependências
│   ├── verificar-ambiente.sh     # Script para verificar variáveis de ambiente
│   └── publicar-google.sh         # Script para publicar no Google
├── src
│   ├── app.ts                   # Ponto de entrada da aplicação
│   └── types
│       └── index.ts             # Tipos e interfaces da aplicação
├── .env.example                  # Exemplo de variáveis de ambiente
├── .gitignore                    # Arquivos a serem ignorados pelo Git
├── package.json                  # Configuração do npm
├── tsconfig.json                 # Configurações do TypeScript
└── README.md                     # Documentação do projeto
```

## Instalação

1. Clone o repositório:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd projeto-publicacao-google
   ```

2. Instale as dependências:
   ```bash
   ./scripts/instalar-dependencias.sh
   ```

## Verificação do Ambiente

Antes de publicar, verifique se todas as variáveis de ambiente necessárias estão definidas:
```bash
./scripts/verificar-ambiente.sh
```

## Publicação

Para publicar a aplicação no Google, execute o seguinte comando:
```bash
./scripts/publicar-google.sh
```

## Contribuição

Sinta-se à vontade para contribuir com melhorias ou correções. Para isso, faça um fork do repositório e envie um pull request.