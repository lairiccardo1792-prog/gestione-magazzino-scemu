# src/modelli/__init__.py

from .prodotti import Categoria, ProdottoBase, ProdottoCreate, ProdottoUpdate, ProdottoResponse
from .ordini import StatoOrdine, OrdineCreate, OrdineResponse
from .generic_res import Messaggio, ErroreDettaglio
from .login import LoginRequest, LoginResponse

__all__ = [
    "Categoria",
    "ProdottoCreate",
    "ProdottoUpdate",
    "ProdottoResponse",
    "StatoOrdine", 
    "OrdineCreate", 
    "OrdineResponse",
    "Messaggio",
    "ErroreDettaglio",
    "LoginRequest",
    "LoginResponse"
]