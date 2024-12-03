# /config/settings.py

import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "my-super-secret-key")  # Lee SECRET_KEY o usa el valor por defecto
    ALGORITHM = os.getenv("ALGORITHM", "HS256")                  # Lee ALGORITHM o usa el valor por defecto
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # Convierte a entero

settings = Settings()