 # src/crud/crud_prodotti.py

from datetime       import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy     import select

from src.servizi.modelli import ProdottiDB as pr
from src.servizi.modelli import OrdiniDB as ord
from src.servizi.modelli import RigaOrdineDB as rgo


# Helper (mapper in java)
def _to_dict(p: pr) -> dict:
    return {
        "id":          p.id,
        "nome":        p.nome,
        "descrizione": p.descrizione,
        "prezzo":      p.prezzo,
        "categoria":   p.categoria,
        "stock":       p.stock,
        "attivo":      p.attivo,
        "creato_il":   p.creato_il.isoformat() if p.creato_il else None,
        "aggiornato_il": p.aggiornato_il.isoformat() if p.aggiornato_il else None,        
    }

# READ
def get_tutti_prodotti(db: Session) -> list[dict]:
    stmt = select(pr).order_by(pr.nome)
    return [_to_dict(p) for p in db.scalars(stmt).all()]

def get_prodotto_by_id(db: Session, prodotto_id) -> dict | None:
    p = db.get(pr, prodotto_id)
    return _to_dict(p) if p else None


# CREATE
def crea_prodotto(db: Session, dati: dict) -> dict:
    categoria=dati["categoria"]
    if not isinstance(categoria, str):
        categoria = categoria.value

    nuovo = pr(
        nome        = dati["nome"],
        descrizione = dati.get("descrizione"),
        prezzo      = dati["prezzo"],
        categoria   = categoria,
        stock       = dati.get("stock", 0),
        attivo      = dati.get("attivo", 1)
    )
    
    db.add(nuovo)
    db.flush()
    db.commit()   # <--- Salva definitivamente le modifiche

    db.refresh(nuovo)

    return _to_dict(nuovo)

# UPDATE
def aggiorna_prodotto(db: Session, prodotto_id: int, dati: dict) -> dict | None:
    p = db.get(pr, prodotto_id)
    if not p:
        return None
    
    if not dati:
        return _to_dict(p)
    
    if "categoria" in dati and not isinstance(dati["categoria"], str):
        dati["categoria"] = dati["categoria"].value

    for campo, valore in dati.items():
        if hasattr(p, campo):
            setattr(p, campo, valore)

    p.aggiornato_il = datetime.now(timezone.utc)
    db.flush()
    db.commit()   # <--- Salva definitivamente le modifiche
    db.refresh(p)

    return _to_dict(p)

# DELETE
def elimina_prodotto(db: Session, prodotto_id: int) -> bool:
    p = db.get(pr, prodotto_id)
    if not p:
        return False

    db.delete(p)
    db.commit()   # <--- Salva definitivamente le modifiche
    db.flush()
    return True 

########################## AGGIUNTA PER ELIMINAZIONE :

def get_ordini_attivi_per_prodotto(db : Session , prodotti_id : int )-> dict | None:
    stmt = (select(ord).join(rgo).where(rgo.prodotti_id == prodotti_id,
    ord.stato.notin_(["consegnato", "annullato"])))
    risultato = db.scalars(stmt).first()
    if not risultato : return None 
    return risultato


    
