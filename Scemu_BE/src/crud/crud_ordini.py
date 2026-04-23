from datetime       import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy     import select

from src.servizi.modelli import OrdiniDB as ord
from src.servizi.modelli import RigaOrdineDB as rod

# HELPER
def _riga_to_dict(r: rod) -> dict:
    return {
        "id":              r.id,
        "prodotto_id":     r.prodotti_id,
        "nome_prodotto":   r.nome_prodotto,
        "prezzo_unitario": r.prezzo_unitario,
        "quantita":        r.quantita,
        "subtotale":       r.subtotale
    }

def _to_dict(o: ord) -> dict:
    return {
        "id":            o.id,
        "utente_id":     o.utente_id,  # <--- AGGIUNTO: utile per i controlli di sicurezza
        "cliente_nome":  o.cliente_nome,
        "cliente_email": o.cliente_email,
        "totale":        o.totale,
        "stato":         o.stato,
        "note":          o.note,
        "righe":         [_riga_to_dict(r) for r in o.righe],
        "creato_il":     o.creato_il.isoformat() if o.creato_il else None,
        "aggiornato_il": o.aggiornato_il.isoformat() if o.aggiornato_il else None,
    }

# READ
def get_tutti_ordini(db: Session) -> list[dict]:
    stmt = select(ord).order_by(ord.creato_il)
    return [_to_dict(o) for o in db.scalars(stmt).all()]

# NUOVA FUNZIONE: Questa è quella che usa la rotta per filtrare
def get_ordini_per_utente(db: Session, utente_id: int) -> list[dict]:
    """Recupera solo gli ordini appartenenti a un determinato utente"""
    stmt = select(ord).where(ord.utente_id == utente_id).order_by(ord.creato_il.desc())
    return [_to_dict(o) for o in db.scalars(stmt).all()]

def get_ordine_by_id(db: Session, ordine_id: int) -> dict | None:
    o = db.get(ord, ordine_id)
    return _to_dict(o) if o else None

# CREATE
def crea_ordine(db: Session, dati: dict) -> dict:
    nuovo_ordine = ord(
        utente_id     = dati["utente_id"],  # <--- AGGIUNTO: salviamo chi ha fatto l'ordine
        cliente_nome  = dati["cliente_nome"],
        cliente_email = dati["cliente_email"],
        totale        = dati["totale"],
        stato         = dati["stato"],
        note          = dati.get("note"),
    )
    db.add(nuovo_ordine)
    db.flush() # Otteniamo l'ID dell'ordine appena creato

    for riga in dati["righe"]:
        db.add(rod(
            ordini_id       = nuovo_ordine.id,
            prodotti_id     = riga["prodotto_id"],
            nome_prodotto   = riga["nome_prodotto"],
            prezzo_unitario = riga["prezzo_unitario"],
            quantita        = riga["quantita"],
            subtotale       = riga["subtotale"]   
        ))

    db.commit()   # Salva tutto: ordine e righe
    db.refresh(nuovo_ordine)

    return _to_dict(nuovo_ordine)

# UPDATE STATO
def aggiorna_stato_ordine(db: Session, ordine_id: int, nuovo_stato: str) -> dict | None:
    o = db.get(ord, ordine_id)
    if not o:
        return None
    
    o.stato         = nuovo_stato
    o.aggiornato_il = datetime.now(timezone.utc)
    db.commit()
    db.refresh(o)

    return _to_dict(o)