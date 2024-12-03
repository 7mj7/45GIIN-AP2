from pydantic import BaseModel, EmailStr

class User(BaseModel):
    """
    Modelo Pydantic para representar un usuario
    Attributes:
        email: Email del usuario (validado automáticamente)
        password: Contraseña del usuario (en producción usar hash)
    """
    email: EmailStr
    password: str

class Token(BaseModel):
    """
    Modelo Pydantic para el token de autenticación
    Attributes:
        access_token: Token JWT
        token_type: Tipo de token (bearer)
    """
    access_token: str
    token_type: str