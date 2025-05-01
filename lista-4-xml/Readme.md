# 📚 API de Gerenciamento de Livros (FastAPI + XML)

Este projeto implementa uma API RESTful em *FastAPI* para realizar operações de *CRUD de livros, com persistência de dados em um arquivo **XML* (livros.xml).  
Ideal para fins educativos e prática com estrutura de projetos modulares.

---

## 🚀 Tecnologias utilizadas

- Python 3.10+ (recomendado)
- FastAPI
- Uvicorn (servidor ASGI)
- XML (com xml.etree.ElementTree)

---

## 📁 Estrutura do Projeto

. ├── api/ │ 
           ├── app.py # Arquivo principal com o app FastAPI 
           │ 
           ├── models/ # Modelos Pydantic (Livro) 
           │ 
           ├── routes/ # Rotas da API 
           │ 
           └── functions/ # Lógica de leitura/escrita do XML 
           │ 
           ├── db/ │ 
                   └── livros.xml # "Banco de dados" XML 
           │ 
           ├── .venv/ # Ambiente virtual (gitignore) 
           ├── requirements.txt # Dependências do projeto 
           └── README.md

yaml
Copiar
Editar

---

## ⚙️ Como rodar o projeto localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
2. Crie e ative o ambiente virtual
bash
Copiar
Editar
python -m venv .venv
# Ativação no Windows:
.venv\Scripts\Activate.ps1

# Ativação no Linux/macOS:
source .venv/bin/activate
3. Instale as dependências
bash
Copiar
Editar
pip install -r requirements.txt
4. Rode o servidor
bash
Copiar
Editar
uvicorn api.app:app --reload
Acesse:

Swagger UI: http://127.0.0.1:8000/docs

Redoc: http://127.0.0.1:8000/redoc


🧪 Exemplos de uso
POST /livros
json
Copiar
Editar
{
  "id": 1,
  "titulo": "Dom Quixote",
  "autor": "Miguel de Cervantes",
  "ano": 1605,
  "genero": "Romance"
}
GET /livros
Lista todos os livros cadastrados.

GET /livros/{id}
Busca um livro pelo id.

PUT /livros/{id}
Atualiza as informações de um livro específico.

DELETE /livros/{id}
Remove o livro do arquivo XML.

📄 Licença
Este projeto é livre para fins acadêmicos e educativos.