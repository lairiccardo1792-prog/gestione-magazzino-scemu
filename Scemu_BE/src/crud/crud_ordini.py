# src/crud/crud_ordini.py

from datetime import datetime
from src.servizi.database import get_connection
from src.utility.utils import converti_riga, converti_righe

def get_tutti_ordini(skip: int = 0, limit: int = 100) -> list:
    conn = get_connection()
    cursore = conn.cursor(dictionary=True)

    try:
        cursore.execute(
            "SELECT * FROM ordini ORDER BY id LIMIT %s OFFSET %s",
            (limit, skip)
        )
        ordini = cursore.fetchall()
        return [_add_righe(o, cursore) for o in ordini]
    finally:
        cursore.close()
        conn.close()

def get_ordine_by_id(ordini_id: int) -> dict | None:
    conn = get_connection()
    cursore = conn.cursor(dictionary=True)

    try:
        cursore.execute("SELECT * FROM ordini WHERE id = %s", (ordini_id, ))
        ordine = cursore.fetchone()
        
        if not ordine:
            return None
        return _add_righe(ordine, cursore)
    finally:
        cursore.close()
        conn.close()    

def crea_ordine(dati: dict) -> dict:
    conn = get_connection()
    cursore = conn.cursor(dictionary=True)

    try:
        cursore.execute("INSERT INTO ordini (utente_id, cliente_nome, cliente_email, totale, stato, note) "
                        "VALUES (%s, %s, %s, %s, %s, %s)",
                        (dati.get("utente_id", 1),
                         dati["cliente_nome"],
                         dati["cliente_email"],
                         dati["totale"],
                         dati["stato"],
                         dati.get("note")))
        ordini_id = cursore.lastrowid

        for riga in dati["righe"]:
            cursore.execute("INSERT INTO righe_ordini (ordini_id, prodotti_id, nome_prodotto, prezzo_unitario, quantita, sub_totale) "
                            "VALUES (%s, %s, %s, %s, %s, %s)",
                            (ordini_id,
                             riga["prodotto_id"],
                             riga["nome_prodotto"],
                             riga["prezzo_unitario"],
                             riga["quantita"],
                             riga["subtotale"]))
        conn.commit()    
        
        cursore.execute("SELECT * FROM ordini WHERE id = %s", (ordini_id, ))
        ordine = cursore.fetchone()
        
        return _add_righe(ordine, cursore)
    except:
        conn.rollback()
        raise
    finally:
        cursore.close()
        conn.close()    

def aggiorna_stato_ordine(ordini_id: int, nuovo_stato: str) -> dict | None:
    conn = get_connection()
    cursore = conn.cursor(dictionary=True)

    try:
        cursore.execute("UPDATE ordini SET stato = %s, aggiornato_il = %s WHERE id = %s",
                        (nuovo_stato, datetime.now(), ordini_id))
        conn.commit()

        cursore.execute("SELECT * FROM ordini WHERE id = %s", (ordini_id, ))
        ordine = cursore.fetchone()
        
        if not ordine:
            return None
        return _add_righe(ordine, cursore)
    finally:
        cursore.close()
        conn.close()    

# --- HELPER INTERNO -------------------------------------
def _add_righe(ordine: dict, cursor) -> dict:
    cursor.execute(
        "SELECT * FROM righe_ordini WHERE ordini_id = %s ORDER BY id", (ordine["id"], ))
    
    righe  = cursor.fetchall()
    ordine = dict(ordine)
    ordine["righe"] = converti_righe(righe)
    return converti_riga(ordine)
