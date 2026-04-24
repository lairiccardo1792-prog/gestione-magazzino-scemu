# src/crud/crud_prodotti.py

from datetime import datetime
from src.servizi.database import get_connection
from src.utility.utils import converti_riga, converti_righe

def get_tutti_prodotti() -> list:
    conn = get_connection()
    cursore = conn.cursor(dictionary=True)

    try:
        cursore.execute("SELECT * FROM prodotti ORDER BY nome")
        return converti_righe(cursore.fetchall())
    finally:
        cursore.close()
        conn.close()

def get_prodotto_by_id(prodotto_id: int) -> dict | None:
    conn = get_connection()
    cursore = conn.cursor(dictionary=True)

    try:
        cursore.execute("SELECT * FROM prodotti WHERE id = %s", (prodotto_id,))
        row = cursore.fetchone()

        return converti_riga(row) if row else None
    finally:
        cursore.close()
        conn.close()

def crea_prodotto(dati: dict) -> dict:
    conn = get_connection()
    cursore = conn.cursor(dictionary=True)

    try:
        cursore.execute("INSERT INTO prodotti (nome, descrizione, prezzo, categoria, stock, attivo) "
                        "VALUES (%s, %s, %s, %s, %s, %s)", (
                            dati["nome"],
                            dati.get("descrizione"),
                            dati["prezzo"],
                            dati["categoria"] if isinstance(dati["categoria"], str) else dati["categoria"].value,
                            dati["stock"],
                            1 if dati["attivo"] else 0
                        ))
        conn.commit()
        cursore.execute("SELECT * FROM prodotti WHERE id = %s", (cursore.lastrowid,))
        return converti_riga(cursore.fetchone())       
    finally:
        cursore.close()
        conn.close()

def aggiorna_prodotto(prodotto_id: int, dati: dict) -> dict | None:
    conn = get_connection()
    cursore = conn.cursor(dictionary=True)
    
    # UPDATE prodotti SET <campi> WHERE id = %s"
    # campo = %s

    if not dati:
        return get_prodotto_by_id(prodotto_id)

    try:
        if "categoria" in dati and not isinstance(dati["categoria"], str):
            dati["categoria"] = dati["categoria"].value

        set_campi = ", ".join(f"{campo} = %s" for campo in dati.keys())
        valori = list(dati.values()) + [datetime.now(), prodotto_id]
        cursore.execute(f"UPDATE prodotti SET {set_campi}, aggiornato_il = %s WHERE id = %s",
                        valori)
        
        conn.commit()
        cursore.execute("SELECT * FROM prodotti WHERE id = %s", (prodotto_id,))
        row = cursore.fetchone()

        return converti_riga(row) if row else None 
    finally:
        cursore.close()
        conn.close()

def elimina_prodotto(prodotto_id: int) -> bool:
    conn = get_connection()
    cursore = conn.cursor(dictionary=True)

    try:
        cursore.execute("DELETE FROM prodotti WHERE id = %s", (prodotto_id,))
        conn.commit()
        return cursore.rowcount > 0
    finally:
        cursore.close()
        conn.close()