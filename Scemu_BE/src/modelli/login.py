# src/modelli/login.py

from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    """Modello per la richiesta di login"""
    user: str = Field(..., min_length=1, description="Username")
    password: str = Field(..., min_length=1, description="Password")

class LoginResponse(BaseModel):
    """Modello per la risposta di login"""
    success: bool = Field(..., description="Successo dell'autenticazione")
    message: str = Field(..., description="Messaggio di risposta")
    username: str | None = Field(None, description="Username dell'utente autenticato")
    token: str | None = Field(None, description="JWT token valido 24h")
