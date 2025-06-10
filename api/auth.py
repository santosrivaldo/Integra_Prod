from fastapi import HTTPException, Header
import os

API_TOKEN = os.getenv("API_TOKEN", "my_secure_token")

def validate_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Formato de token inválido")
    token = authorization.split(" ")[1]
    if token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Token inválido")