from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated, Dict
from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta
from models.user import User, Token  # Asume que moves los modelos a models/
from config.settings import settings

# OAuth2 setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Simulated DB (move to a database module in production)
users_db: Dict[str, User] = {
    "user1@example.com": User(email="user1@example.com", password="1234"),
    "user2@example.com": User(email="user2@example.com", password="abcd"),
}

def create_access_token(data: dict) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({"exp": expires})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("email")
        if not email or email not in users_db:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return users_db[email]
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

async def login_user(form_data: OAuth2PasswordRequestForm) -> Token:
    user = users_db.get(form_data.username)
    if not user or form_data.password != user.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({"email": user.email})
    return Token(access_token=access_token, token_type="bearer")