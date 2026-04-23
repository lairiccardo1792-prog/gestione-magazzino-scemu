# src\modelli\utenti.py

from pydantic import BaseModel


class LoginRequest(BaseModel):
    user: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    username: str | None = None 
    token :str | None = None 



