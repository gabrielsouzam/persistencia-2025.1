import os
import xml.etree.ElementTree as ET
from typing import List
from fastapi import HTTPException
from api.models.livro_model import Livro

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO_XML = os.path.join(BASE_DIR, "db", "livros.xml")

def inicializar_xml():
    if not os.path.exists("db"):
        os.makedirs("db")

    if not os.path.exists(CAMINHO_XML) or os.path.getsize(CAMINHO_XML) == 0:
        root = ET.Element("livros")
        tree = ET.ElementTree(root)
        tree.write(CAMINHO_XML, encoding="utf-8", xml_declaration=True)

def ler_livros() -> List[Livro]:
    tree = ET.parse(CAMINHO_XML)
    root = tree.getroot()
    livros = []
    for elem in root.findall("livro"):
        livros.append(Livro(
            id=int(elem.find("id").text),
            titulo=elem.find("titulo").text,
            autor=elem.find("autor").text,
            ano=int(elem.find("ano").text),
            genero=elem.find("genero").text
        ))
    return livros

def salvar_livros(livros: List[Livro]):
    root = ET.Element("livros")
    for livro in livros:
        elem = ET.SubElement(root, "livro")
        ET.SubElement(elem, "id").text = str(livro.id)
        ET.SubElement(elem, "titulo").text = livro.titulo
        ET.SubElement(elem, "autor").text = livro.autor
        ET.SubElement(elem, "ano").text = str(livro.ano)
        ET.SubElement(elem, "genero").text = livro.genero
    tree = ET.ElementTree(root)
    tree.write(CAMINHO_XML)

def listar_livros():
    return ler_livros()

def buscar_livro(livro_id: int):
    livros = ler_livros()
    for livro in livros:
        if livro.id == livro_id:
            return livro
    raise HTTPException(status_code=404, detail="Livro não encontrado")

def criar_livro(novo_livro: Livro):
    livros = ler_livros()
    if any(l.id == novo_livro.id for l in livros):
        raise HTTPException(status_code=400, detail="ID já existente")
    livros.append(novo_livro)
    salvar_livros(livros)
    return {"mensagem": "Livro criado com sucesso"}

def atualizar_livro(livro_id: int, livro_atualizado: Livro):
    livros = ler_livros()
    for idx, livro in enumerate(livros):
        if livro.id == livro_id:
            livros[idx] = livro_atualizado
            salvar_livros(livros)
            return {"mensagem": "Livro atualizado"}
    raise HTTPException(status_code=404, detail="Livro não encontrado")

def deletar_livro(livro_id: int):
    livros = ler_livros()
    livros_novos = [livro for livro in livros if livro.id != livro_id]
    if len(livros) == len(livros_novos):
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    salvar_livros(livros_novos)
    return {"mensagem": "Livro deletado"}
