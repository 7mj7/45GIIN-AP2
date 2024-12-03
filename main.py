# main.py

# Importaciones necesarias
from fastapi import FastAPI
from api.v1 import endpoints as v1_endpoints
# from api.v2 import endpoints as v2_endpoints  # Si alguna vez tenemos v2


# Inicialización de la aplicación FastAPI
app = FastAPI(title="API Simple con Autenticación")

# Registro del router de autenticación
app.include_router(
    v1_endpoints.router,
     prefix="/api/v1",      # Añadimos el prefijo aquí
    # tags=["v1"]           # El tag lo añadimos en v1/endpoints.py
)

# Versión 2 (cuando la tengamos)
# app.include_router(
#     v2_endpoints.router,
#     prefix="/api/v2",
#     tags=["v2"]
# )

# Ruta raíz de la API
@app.get("/")
async def root():
    return {"message": "Bienvenido a mi API"}