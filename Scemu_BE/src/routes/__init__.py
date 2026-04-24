# src/routes/__init__.py
from . import routes_ordini
from . import routes_prodotti
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