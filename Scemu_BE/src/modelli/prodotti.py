# src/modelli/prodotti.py

from pydantic import BaseModel, Field, field_validator
from typing   import Optional
from datetime import datetime
from enum     import Enum

class Categoria(str, Enum):
    # Categorie prodotti
    ELETTRONICA   = "Elettronica"
    ABBIGLIAMENTO = "Abbigliamento"
    ALIMENTARI    = "Alimentari"
    LIBRI         = "Libri"
    SPORT         = "Sport"
    ALTRO         = "Altro"

class ProdottoBase(BaseModel):
    nome: str        = Field(..., min_length=3, max_length=500)
    descrizione: str = Field(..., min_length=2, max_length=500)
    prezzo: float    = Field(..., gt=0)
    categoria: Categoria
    stock: int       = Field(default=0, ge=0)
    attivo: bool     = Field(default=True)

    @field_validator("prezzo")
    @classmethod
    def arrotonda_prezzo(cls, v):
        return round(v, 2)

class ProdottoCreate(ProdottoBase):
    pass

class ProdottoUpdate(BaseModel):
    nome:        Optional[str]       = Field(None, min_length=3, max_length=500)
    descrizione: Optional[str]       = None
    prezzo:      Optional[float]     = Field(None, gt=0)
    categoria:   Optional[Categoria] = None
    stock:       Optional[int]       = Field(None, ge=0)
    attivo:      Optional[bool]      = None

class ProdottoResponse(ProdottoBase):
    id: int
    creato_il: str
    aggiornato_il: Optional[str] = None

    class Config:
        json_schema_extra = {"example":{
            "id": 1,
            "nome": "Mac Pro (Non quello della D.)",
            "descrizione": "L'unico Mac scarso del pianeta",
            "prezzo": 1299.99,
            "categoria": "Elettronica",
            "stock": 10,
            "attivo": True,
            "creato_il": "2026-03-14T14:35:00",
            "aggiornato_il": "2026-04-14T10:21:00",            
        }}