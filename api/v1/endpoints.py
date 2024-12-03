from fastapi import APIRouter
from api.v1.routes import auth_routes  # Importación ajustada a la estructura real

router = APIRouter()
router.include_router(
    auth_routes.router,
    tags=["v1/Authentication"]  # Agregamos el prefijo v1 al tag
)