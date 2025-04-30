from fastapi import APIRouter
from api.models.livro_model import Livro
from api.functions import livro_functions as database

router = APIRouter()

@router.get("/livros")
def listar():
    return database.listar_livros()

@router.get("/livros/{livro_id}")
def buscar(livro_id: int):
    return database.buscar_livro(livro_id)

@router.post("/livros")
def criar(livro: Livro):
    return database.criar_livro(livro)

@router.put("/livros/{livro_id}")
def atualizar(livro_id: int, livro: Livro):
    return database.atualizar_livro(livro_id, livro)

@router.delete("/livros/{livro_id}")
def deletar(livro_id: int):
    return database.deletar_livro(livro_id)
