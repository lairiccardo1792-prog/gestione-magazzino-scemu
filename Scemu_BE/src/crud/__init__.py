# src/crud/__init__.py

from .crud_ordini import get_tutti_ordini, get_ordine_by_id, crea_ordine, aggiorna_stato_ordine
from .crud_prodotti import get_tutti_prodotti, get_prodotto_by_id, crea_prodotto, aggiorna_prodotto, elimina_prodotto
from .crud_utenti import get_utente_by_username, verify_password

__all__ = [
    "get_tutti_ordini", 
    "get_ordine_by_id", 
    "crea_ordine", 
    "aggiorna_stato_ordine",
    "get_tutti_prodotti", 
    "get_prodotto_by_id", 
    "crea_prodotto", 
    "aggiorna_prodotto", 
    "elimina_prodotto",
    "get_utente_by_username",
    "verify_password"    
]