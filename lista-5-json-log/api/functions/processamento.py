import json
import yaml
import logging
from typing import List
from api.models.registro_model import Registro

def carregar_config(path="config/config.yaml"):
  with open(path, 'r') as file:
      return yaml.safe_load(file)

def configurar_logging(config):
  logging.basicConfig(
      filename=config["logging"]["file"],
      level=getattr(logging, config["logging"]["level"]),
      format=config["logging"]["format"]
  )

def carregar_dados_json(path) -> List[dict]:
  with open(path, 'r') as file:
      return json.load(file)

def processar_registros(registros: List[dict]):
  for registro in registros:
      if registro.get("age") is not None:
          logging.info(f"Processando registro: {registro}")
      else:
          logging.warning(f"Erro no registro: Dado inválido: {registro}")
