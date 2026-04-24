# src/routes/routes_prodotti.py

from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional
from src import modelli as md
from src import crud as cr

router = APIRouter(
    prefix="/prodotti",
    tags=["Prodotti"]
)

@router.get("", response_model=dict)
def get_prodotti(
    q:         Optional[str]          = Query (None, description="Cerca nel nome o descrizione"),
    categoria: Optional[md.Categoria] = None,
    min_prezzo: Optional[float]       = Query(None, qe=0),
    max_prezzo: Optional[float]       = Query(None, qe=0),
    solo_disponibili: bool            = Query(False, description="Solo prodotti con stock > 0"),
    skip: int                         = Query(0, ge=0),
    limit: int                        = Query(10, ge=1, le=100),
):
    prodotti = cr.get_tutti_prodotti()

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
def get_prodotto(prodotto_id: int):
    prodotto = cr.get_prodotto_by_id(prodotto_id)

    if not prodotto:
        raise HTTPException(
            status_code=404,
            detail=f"Prodotto {prodotto_id} non trovato"
        )
    return prodotto

@router.post("", response_model=md.ProdottoResponse, status_code=status.HTTP_201_CREATED)
def crea_prodotto(prodotto: md.ProdottoCreate):    
    esistenti = cr.get_tutti_prodotti()
    if any(p["nome"].lower() == prodotto.nome.lower() for p in esistenti):
        raise HTTPException(400, f"Prodotto '{prodotto.nome}' già inserito")
    
    nuovo = cr.crea_prodotto(prodotto.model_dump())
    return nuovo

@router.patch("/{prodotto_id}", response_model=md.ProdottoResponse)
def aggiorna_prodotto(prodotto_id:int, dati: md.ProdottoUpdate):

    if not cr.get_prodotto_by_id(prodotto_id):
        raise HTTPException(404, "Prodotto non trovato")

    aggiornamento = dati.model_dump(exclude_none=True)
    if not aggiornamento:
       raise HTTPException(status_code=400, detail="Nessun campo da aggiornare")

    aggiornato = cr.aggiorna_prodotto(prodotto_id, aggiornamento)
    return aggiornato 

@router.delete("/{prodotto_id}", status_code=status.HTTP_204_NO_CONTENT)
def elimina_prodotto(prodotto_id: int):
    if not cr.get_prodotto_by_id(prodotto_id):
        raise HTTPException(404, "Prodotto non trovato")
    
    ordini = cr.get_tutti_ordini()
    ordini_attivi = [
        o for o in ordini
        if o["stato"] not in ["consegnato", "annullato"]
        and any((r.get("prodotto_id") or r.get("prodotti_id")) == prodotto_id for r in o["righe"])
    ]

    if ordini_attivi:
        raise HTTPException(
            status_code=400,
            detail=f"Impossibile eliminare: prodotto presenti in {len(ordini_attivi)} ordini attivi"            
        )
    
    cr.elimina_prodotto(prodotto_id)