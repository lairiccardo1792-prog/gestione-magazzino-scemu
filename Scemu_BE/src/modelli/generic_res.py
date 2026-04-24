# src/modelli/generic_res.py

from pydantic import BaseModel
from typing   import Optional

class Messaggio(BaseModel):
    messaggio: str

class ErroreDettaglio(BaseModel):
    errore: str
    dettaglio: Optional[str] = None