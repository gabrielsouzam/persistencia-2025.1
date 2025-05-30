from fastapi import APIRouter
from . import membro_routes, projeto_routes, tarefa_routes, equipe_routes

router = APIRouter()

router.include_router(membro_routes.router)
router.include_router(projeto_routes.router)
router.include_router(tarefa_routes.router)
router.include_router(equipe_routes.router)
