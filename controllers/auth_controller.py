# Importaciones necesarias
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated, Dict
from jose import jwt, JWTError  # Para manejo de tokens JWT
from datetime import datetime, timezone, timedelta
from models.user import User, Token
from config.settings import settings

# Configuración del esquema OAuth2
# tokenUrl="token" indica el endpoint donde se realizará la autenticación
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Base de datos simulada de usuarios
# En producción, esto debería estar en una base de datos real
users_db: Dict[str, User] = {
    "user1@example.com": User(email="user1@example.com", password="1234"),
    "user2@example.com": User(email="user2@example.com", password="abcd"),
}

def create_access_token(data: dict) -> str:
    """
    Crea un token JWT con los datos proporcionados
    Args:
        data (dict): Datos a codificar en el token
    Returns:
        str: Token JWT generado
    """
    # Calcula la fecha de expiración del token
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # Copia los datos y añade la fecha de expiración
    to_encode = data.copy()
    to_encode.update({"exp": expires})
    # Genera y retorna el token JWT firmado
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """
    Valida el token JWT y retorna el usuario actual
    Args:
        token (str): Token JWT a validar
    Returns:
        User: Usuario autenticado
    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    """
    try:
        # Decodifica el token JWT
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        # Extrae el email del payload
        email = payload.get("email")
        # Verifica que el email existe y está en la base de datos
        if not email or email not in users_db:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return users_db[email]
    except JWTError:
        # Si hay error al decodificar el token
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

async def login_user(form_data: OAuth2PasswordRequestForm) -> Token:
    """
    Autentica un usuario y genera un token JWT
    Args:
        form_data (OAuth2PasswordRequestForm): Formulario con username y password
    Returns:
        Token: Token de acceso generado
    Raises:
        HTTPException: Si las credenciales son inválidas
    """
    # Busca el usuario en la base de datos
    user = users_db.get(form_data.username)
    # Verifica las credenciales
    if not user or form_data.password != user.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # Genera el token de acceso
    access_token = create_access_token({"email": user.email})
    # Retorna el token con su tipo
    return Token(access_token=access_token, token_type="bearer")