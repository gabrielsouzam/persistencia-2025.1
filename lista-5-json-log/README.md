# Projeto: Processamento de JSON e Registro de Logs

Este projeto é uma API construída em Python para processar dados de um arquivo JSON, registrar informações relevantes em log, e fornecer endpoints para interagir com os dados.

## Tecnologias Utilizadas

- Python 3.12+
- Flask
- PyYAML
- Logging

## Estrutura do Projeto

```
lista-5-json-log/
├── api/
│   ├── app.py                  # Arquivo principal da aplicação Flask
│   ├── functions/              # Funções de processamento
│   ├── models/                 # Modelos de dados
│   └── routes/                 # Rotas da API
├── config/
│   └── config.yaml             # Configurações da aplicação
├── data/
│   └── data.json               # Arquivo de entrada com os dados em JSON
├── logs/
│   └── app.log                 # Arquivo de log da aplicação
├── requirements.txt            # Dependências do projeto
└── .gitignore
```

## Como Executar

1. **Clone o repositório e acesse a pasta:**
   ```git clone <url-do-repositorio>
      cd lista-5-json-log
   ```

2. **Instale as dependências:**
   ```pip install -r requirements.txt
   ```

3. **Execute a aplicação:**
   ```uvicorn api.app:app --reload
   ```

   A API será iniciada em `http://localhost:8000`.

## Endpoints

Exemplos de rotas (baseados na estrutura dos arquivos):

- `GET /processar`: Inicia o processamento do arquivo JSON.
