from fastapi import FastAPI
from api.routes import livro_routes
from api.functions.livro_functions import inicializar_xml

app = FastAPI()
inicializar_xml()

app.include_router(livro_routes.router)
