from fastapi import APIRouter
from api.functions import processamento

router = APIRouter()

@router.get("/processar")
def executar_processamento():
    config = processamento.carregar_config()
    processamento.configurar_logging(config)
    registros = processamento.carregar_dados_json(config["data"]["file"])
    processamento.processar_registros(registros)
    return {"mensagem": "Processamento executado. Veja logs em app.log."}
