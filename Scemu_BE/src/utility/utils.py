# src/utility/utils.py

from datetime import datetime

def converti_riga(row: dict) -> dict:
    if row is None:
        return None
    
    risultato = {}
    for k, v in row.items():
        if isinstance(v, datetime):
            risultato[k] = v.isoformat()
        elif hasattr(v, "__float__"):
            risultato[k] = float(v)
        elif k == 'attivo':
            risultato[k] = True if v > 0 else False    
        else:
            risultato[k] = v
    return risultato                

def converti_righe(rows: list) -> list:
    return [converti_riga(r) for r in rows]