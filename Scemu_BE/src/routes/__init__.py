# src/routes/__init__.py
from .routes_ordini import crea_ordine, get_ordini, get_ordine, aggiorna_stato
from .routes_prodotti import get_prodotti, get_prodotto, crea_prodotto, aggiorna_prodotto, elimina_prodotto

__all__ = [
    "crea_ordine", 
    "get_ordini", 
    "get_ordine", 
    "aggiorna_stato",
    "get_prodotti", 
    "get_prodotto", 
    "crea_prodotto", 
    "aggiorna_prodotto", 
    "elimina_prodotto"
]