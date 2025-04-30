from typing import Union
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import xml.etree.ElementTree as ET
from http import HTTPStatus
import csv
import os

app = FastAPI()
CSV_FILE = "database.csv"

class Produto(BaseModel):
    id: int
    nome: str
    preco: float
    quantidade: int
    
def ler_dados_xml():
  produtos = []
  if os.path.exists("db/produtos.xml"):
    tree = ET.parse("db/produtos.xml")
  root = tree.getroot()
  for elem in root.findall("produto"):
      produto = Produto(
        id=int(elem.find("id").text),
        nome=elem.find("nome").text,
        preco=float(elem.find("preco").text),
        quantidade=int(elem.find("quantidade").text)
    )   
  produtos.append(produto)
  return produtos

def escrever_dados_xml(produtos):
  root = ET.Element("produtos")
  for produto in produtos:
    produto_elem = ET.SubElement(root, "produto")
    ET.SubElement(produto_elem, "id").text = str(produto.id)
    ET.SubElement(produto_elem, "nome").text = produto.nome
    ET.SubElement(produto_elem, "preco").text = str(produto.preco)
    ET.SubElement(produto_elem, "quantidade").text = str(produto.quantidade)
  tree = ET.ElementTree(root)
  tree.write("db/produtos.xml")
            
@app.get("/produtos", response_model=List[Produto])
def listar_produtos():
    return ler_dados_xml()

@app.get("/produtos/{produto_id}", response_model=Produto)
def obter_produto(produto_id: int):
    produtos = listar_produtos()
    for produto in produtos:
        if produto.id == produto_id:
            return produto
    raise HTTPException(status_code=404, 
                        detail="Produto não encontrado")
    
@app.post("/produtos", response_model=Produto)
def criar_produto(produto: Produto):
    produtos = listar_produtos()
    if any(p.id == produto.id for p in produtos):
        raise HTTPException(status_code=400, detail="Id já existe")
    produtos.append(produto)
    escrever_dados_xml(produtos)
    return produto

@app.put("/produtos/{produto_id}", response_model=Produto)
def atualizar_produto(produto_id: int, produto_atualizado: Produto):
    produtos = listar_produtos()
    for i, produto in enumerate(produtos):
        if produto.id == produto_id:
            produtos[i] = produto_atualizado
            escrever_dados_xml(produtos)
            return produto_atualizado
    raise HTTPException(status_code=404, detail="Produto não encontrado")

@app.delete("/produtos/{produto_id}", response_model=dict)
def deletar_produto(produto_id: int):
    produtos = listar_produtos()
    produtos_filtrados = [produto for produto in produtos 
                          if produto.id != produto_id]
    if len(produtos) == len(produtos_filtrados):
        raise HTTPException(status_code=404, 
                            detail="Produto não encontrado")
    escrever_dados_xml(produtos_filtrados)
    return {"mensagem": "Produto deletado com sucesso"}
    
