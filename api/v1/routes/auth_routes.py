from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from controllers.auth_controller import login_user, get_current_user
from models.user import User, Token

router = APIRouter()

@router.post("/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Endpoint para autenticación de usuarios
    - Ruta: /token
    - Método: POST
    - Espera: formulario con username y password
    - Retorna: Token JWT
    """
    return await login_user(form_data)

@router.get("/users/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Endpoint protegido que muestra información del usuario actual
    - Ruta: /users/me
    - Método: GET
    - Requiere: Token JWT válido en header Authorization
    - Retorna: Datos del usuario autenticado
    """
    return current_user