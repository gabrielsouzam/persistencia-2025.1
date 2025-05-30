# API de Blog Pessoal

API RESTful de Blog Pessoal usando FastAPI, SQLModel e SQLite.

## Entidades

- User
- Post
- Category
- Comment
- Like

## Funcionalidades

- CRUD automático para todas as entidades (fastapi-crudrouter)
- Relacionamentos 1:N e N:M
- Paginação, busca e filtros em posts
- Listagem dos posts mais comentados

## Como rodar

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\Activate.ps1 # Windows PowerShell
pip install -r requirements.txt
uvicorn app.main:app --reload
```