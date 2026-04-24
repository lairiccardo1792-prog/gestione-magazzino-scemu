# src/utility/utils.py

from datetime import datetime

def converti_riga(row: dict) -> dict:
    if row is None:
        return None
    
    risultato = {}
    for k, v in row.items():
        # Normalizza nomi colonne: prodotti_id → prodotto_id (per coerenza)
        k_normalizzato = "prodotto_id" if k == "prodotti_id" else k
        
        if isinstance(v, datetime):
            risultato[k_normalizzato] = v.isoformat()
        elif hasattr(v, "__float__"):
            risultato[k_normalizzato] = float(v)
        elif k_normalizzato == 'attivo':
            risultato[k_normalizzato] = True if v > 0 else False    
        else:
            risultato[k_normalizzato] = v
    return risultato                

def converti_righe(rows: list) -> list:
    return [converti_riga(r) for r in rows]