# src/routes/routes_prodotti.py

from fastapi        import APIRouter, HTTPException, status, Query, Depends
from sqlalchemy.orm import Session
from typing         import Optional

import modelli as md
import src.crud.crud_prodotti as cr  # Oppure come hai chiamato il tuo file crud
from src.servizi.database import get_db

router = APIRouter (
    prefix = "/prodotti",
    tags= ["Prodotti"]
)

# Get Lista
@router.get("", response_model=dict)
def get_prodotti(
    q:                Optional[str]          = Query (None, description="Cerca nel nome o descrizione"),
    categoria:        Optional[md.Categoria] = None,
    min_prezzo:       Optional[float]        = Query(None, ge=0),
    max_prezzo:       Optional[float]        = Query(None, ge=0),
    solo_disponibili: bool                   = Query(False, description="Solo prodotti con stock > 0"),
    skip:             int                    = Query(0, ge=0),
    limit:            int                    = Query(10, ge=1, le=100),
    db:               Session                = Depends(get_db)
):
    prodotti = cr.get_tutti_prodotti(db)

    # filtro attivi
    prodotti = [p for p in prodotti if p.get("attivo") > 0]

    # ricerca testuale
    if q:
        q_lower = q.lower()
        prodotti = [p for p in prodotti 
                    if q_lower in p["nome"].lower()
                    or q_lower in (p.get("descrizione") or "").lower()]

    # filtro categoria
    if categoria:
        prodotti =[p for p in prodotti if p["categoria"] == md.Categoria.value]

    # filtro prezzo
    if min_prezzo is not None:
        prodotti =[p for p in prodotti if p["prezzo"] >= min_prezzo]        
    if max_prezzo is not None:
        prodotti =[p for p in prodotti if p["prezzo"] <= max_prezzo]

    # filtro disponibilità
    if solo_disponibili:
        prodotti =[p for p in prodotti if p["stock"] >= 0]

    totale = len(prodotti)
    return {
        "totale":   totale,
        "skip":     skip,
        "limit":    limit,
        "prodotti": prodotti[skip: skip + limit]
    } 










@router.get("/{prodotto_id}", response_model=md.ProdottoResponse)
def get_prodotto(prodotto_id: int, db: Session = Depends(get_db)):
    p = cr.get_prodotto_by_id(db, prodotto_id)
    if not p:
        raise HTTPException(404, f"Prodotto {prodotto_id} non trovato")
    
    return p

# INSERT
@router.post("", response_model=md.ProdottoResponse, status_code=status.HTTP_201_CREATED)
def crea_prodotto(prodotto: md.ProdottoCreate, db: Session = Depends(get_db)):
    esistenti = cr.get_tutti_prodotti(db)
    if any(p["nome"].lower() == prodotto.nome.lower() for p in esistenti):
        raise HTTPException(400, "Prodotto già presente")  
    nuovo = cr.crea_prodotto(db, prodotto.model_dump())
    return nuovo




# PATCH
@router.patch("/{prd}", response_model=md.ProdottoResponse)
def aggiorna_prodotto(prd: int, dati: md.ProdottoUpdate, db: Session = Depends(get_db)):
    if not cr.get_prodotto_by_id(db, prd):
        raise HTTPException(404, "Prodotto non trovato")

    aggiornamento = dati.model_dump(exclude_none=True)
    if not aggiornamento:
       raise HTTPException(status_code=400, detail="Nessun campo da aggiornare")

    aggiornato = cr.aggiorna_prodotto(db, prd, aggiornamento)
    return aggiornato









# PATCH
@router.delete("/{prodotto_id}", status_code=status.HTTP_204_NO_CONTENT)
def elimina_prodotto(prodotto_id: int, db: Session = Depends(get_db)):

    if not cr.get_prodotto_by_id(db, prodotto_id):
        raise HTTPException(404, "Prodotto non trovato")
    

    ordine_bloccante = cr.get_ordini_attivi_per_prodotto(db, prodotto_id)
    
    if ordine_bloccante:
        raise HTTPException(
            status_code=400, 
            detail=f"Impossibile eliminare: prodotto presente nell'ordine #{ordine_bloccante['id']} (Stato: {ordine_bloccante['stato']})"
        )
    
    successo = cr.elimina_prodotto(db, prodotto_id)
    

    if not successo:
        raise HTTPException(status_code=500, detail="Errore durante l'eliminazione del prodotto")


