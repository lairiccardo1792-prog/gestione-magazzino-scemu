# src/modelli/ordini.py

from pydantic import BaseModel, Field, field_validator
from typing   import Optional
from datetime import datetime
from enum     import Enum

class StatoOrdine(str, Enum):
    IN_ATTESA  = "in_attesa"
    CONFERMATO = "confermato" 
    SPEDITO    = "spedito"
    CONSEGNATO = "consegnato"
    ANNULLATO  = "annullato"

class RigaOrdine(BaseModel):
    prodotto_id: int = Field(..., gt=0)
    quantita:    int = Field(..., ge=0) 

class OrdineCreate(BaseModel):
    cliente_nome: str       = Field(..., min_length=2)      
    cliente_email: str      = Field(..., pattern=r"^\S+@\S+\.\S+$")
    righe: list[RigaOrdine] = Field(..., min_length=1)
    note: Optional [str]    = None

    @field_validator("righe")
    @classmethod
    def no_righe_dupplicate(cls, v):
        ids = [r.prodotto_id for r in v]
        if len(ids) != len(set(ids)):
            raise ValueError("Prodotto inserito più volte sullo stesso ordine.")
        return v

class OrdineResponse(BaseModel):
    id:            int    
    cliente_nome:  str
    cliente_email: str
    righe:         list[dict]
    totale:        float
    stato:         StatoOrdine
    note:          Optional[str]
    creato_il:     str
    aggiornato_il: Optional[str] = None   