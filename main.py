# Importaciones necesarias para el funcionamiento
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm  # Para autenticación OAuth2
from typing import Annotated, Dict  # Para tipado más preciso
from jose import jwt, JWTError  # Para manejo de tokens JWT
from pydantic import BaseModel, EmailStr  # Para validación de datos
from datetime import datetime, timedelta, timezone
from config.settings import settings  # Importa settings desde /config/settings.py


# Definición de modelos de datos usando Pydantic
class User(BaseModel):
    email: EmailStr  # Validación automática de formato de email
    password: str    # En producción, nunca almacenar contraseñas en texto plano

class Token(BaseModel):
    access_token: str
    token_type: str  # Siempre será "bearer" en este caso


app = FastAPI(title="API Simple con Autenticación")

# Configuración del esquema OAuth2
# tokenUrl="token" indica el endpoint donde se solicitará el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Base de datos simulada - En producción usar una base de datos real
users_db: Dict[str, User] = {
    "user1@example.com": User(
        email="user1@example.com",
        password="1234"
    ),
    "user2@example.com": User(
        email="user2@example.com",
        password="secret_password"
    )
}

def create_access_token(data: dict) -> str:
    """
    Crea un token JWT con tiempo de expiración
    Args:
        data (dict): Datos a incluir en el token (típicamente el email del usuario)
    Returns:
        str: Token JWT firmado
    """
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({"exp": expires})  # Añade la fecha de expiración al token
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """
    Verifica el token JWT y retorna el usuario actual
    Args:
        token (str): Token JWT a verificar (inyectado automáticamente por FastAPI)
    Returns:
        User: Objeto usuario si el token es válido
    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    """
    try:
        # Decodifica el token y verifica su validez
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("email")
        if not email or email not in users_db:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario inválido"
            )
        return users_db[email]
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar las credenciales"
        )

@app.post("/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Endpoint de login que verifica credenciales y genera token JWT
    Args:
        form_data: Formulario con email (como username) y password
    Returns:
        Token: Objeto con el token de acceso y su tipo
    Raises:
        HTTPException: Si las credenciales son inválidas
    """
    # Busca el usuario por email y verifica la contraseña
    user = users_db.get(form_data.username)
    if not user or form_data.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )
    
    # Genera el token JWT con el email del usuario
    access_token = create_access_token({"email": user.email})
    return Token(access_token=access_token, token_type="bearer")

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Endpoint protegido que requiere autenticación
    Args:
        current_user: Usuario actual (inyectado automáticamente por FastAPI)
    Returns:
        User: Información del usuario actual
    """
    return current_user