# main.py

# Importaciones necesarias
from fastapi import FastAPI, Depends  # FastAPI para crear la API, Depends para inyección de dependencias
from fastapi.security import OAuth2PasswordRequestForm  # Formulario estándar OAuth2 para login
from typing import Annotated  # Para mejorar las anotaciones de tipo
from controllers.auth_controller import login_user, get_current_user  # Funciones de autenticación
from models.user import User, Token  # Modelos Pydantic

# Inicialización de la aplicación FastAPI
app = FastAPI(title="API Simple con Autenticación")

# Endpoint para login
@app.post("/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Endpoint para autenticación de usuarios
    - Ruta: /token
    - Método: POST
    - Espera: formulario con username y password
    - Retorna: Token JWT
    """
    return await login_user(form_data)

# Endpoint protegido que requiere autenticación
@app.get("/users/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Endpoint protegido que muestra información del usuario actual
    - Ruta: /users/me
    - Método: GET
    - Requiere: Token JWT válido en header Authorization
    - Retorna: Datos del usuario autenticado
    """
    return current_user