# src/crud/__init__.py

from .crud_ordini import (
    get_tutti_ordini,
    get_ordini_per_utente,  # <--- AGGIUNGI QUESTA RIGA
    get_ordine_by_id,
    crea_ordine,
    aggiorna_stato_ordine
)

from .crud_prodotti import (
    get_tutti_prodotti,
    get_prodotto_by_id,
    crea_prodotto,
    aggiorna_prodotto,
    elimina_prodotto
)

__all__ = [
    "get_tutti_ordini",
    "get_ordini_per_utente", # <--- AGGIUNGI QUESTA RIGA
    "get_ordine_by_id",
    "crea_ordine",
    "aggiorna_stato_ordine",
    "get_tutti_prodotti",
    "get_prodotto_by_id",
    "crea_prodotto",
    "aggiorna_prodotto",
    "elimina_prodotto"
]