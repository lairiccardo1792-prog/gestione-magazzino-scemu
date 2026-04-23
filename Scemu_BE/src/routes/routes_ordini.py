# src/routes/routes_ordini.py

from fastapi import APIRouter, HTTPException, status, Query, Depends
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import select, and_

import modelli as md
import crud as cr
from src.servizi.database import get_db
# Importiamo il servizio per la gestione del token
from src.servizi.token import get_utente_id_dal_token 
   
router = APIRouter (
    prefix = "/ordini",
    tags= ["Ordini"]
)

_TRANSIZIONI: dict[str, list[str]] = {
    "in_attesa":  ["confermato", "annullato"],
    "confermato": ["spedito", "annullato"],
    "spedito":    ["consegnato"],
    "consegnato": [],
    "annullato":  []
}


@router.post("", response_model=md.OrdineResponse, status_code=status.HTTP_201_CREATED)
def crea_ordine(
    ordine: md.OrdineCreate, 
    db: Session = Depends(get_db),
    utente_id: int = Depends(get_utente_id_dal_token) # <--- Recupero ID dal Token
):
    righe_elaborate = []
    totale          = 0.0
    prodotti_da_aggiornare = []

    # Verifica disponibilità per ogni riga
    for riga in ordine.righe:
        prodotto = cr.get_prodotto_by_id(db, riga.prodotto_id)

        if not prodotto:
            raise HTTPException(404, f"Prodotto {riga.prodotto_id} non trovato")

        if not prodotto.get("attivo", 0) > 0:
            raise HTTPException(400, f"Prodotto '{prodotto['nome']}' non è disponibile")
        
        if prodotto["stock"] < riga.quantita:
            raise HTTPException(400, f"Stock insufficiente per '{prodotto['nome']}' "
                                f"disponibili {prodotto['stock']}, richiesti {riga.quantita}")
        
        subtotale = round(prodotto["prezzo"] * riga.quantita, 2)
        righe_elaborate.append({
            "prodotto_id":     riga.prodotto_id,
            "nome_prodotto":   prodotto["nome"],
            "prezzo_unitario": prodotto["prezzo"],
            "quantita":        riga.quantita,
            "subtotale":       subtotale
        })

        totale += subtotale
        prodotti_da_aggiornare.append({
            "id":          riga.prodotto_id,
            "nuovo_stock": prodotto["stock"] - riga.quantita
        })

    # Crea Ordine: Aggiungiamo utente_id ai dati per il CRUD
    dati_ordine = {
        "utente_id":     utente_id, # <--- Collegamento sicuro all'utente loggato
        "cliente_nome":  ordine.cliente_nome,
        "cliente_email": ordine.cliente_email,
        "righe":         righe_elaborate,
        "totale":        round(totale, 2),
        "stato":         md.StatoOrdine.IN_ATTESA.value,
        "note":          ordine.note
    }

    nuovo_ordine = cr.crea_ordine(db, dati_ordine)

    # Aggiorniamo gli stock
    for p in prodotti_da_aggiornare:
        cr.aggiorna_prodotto(db, p["id"], {"stock": p["nuovo_stock"]})

    return nuovo_ordine

@router.get("", response_model=dict)
def get_ordini(
    stato: Optional[md.StatoOrdine] = None,
    email: Optional[str]            = None, 
    skip:  int                      = 0,
    limit: int                      = Query(10, ge=1, le=100),
    db:    Session                  = Depends(get_db),
    utente_id: int = Depends(get_utente_id_dal_token) # <--- Filtro sicurezza JWT
    ):
    
    # Recuperiamo solo gli ordini che appartengono all'ID dell'utente loggato
    ordini = cr.get_ordini_per_utente(db, utente_id)

    if stato:
        ordini = [o for o in ordini if o["stato"] == stato.value]

    if email:
        ordini = [o for o in ordini if o["cliente_email"] == email]

    return {
        "totale": len(ordini),
        "ordini": ordini[skip: skip + limit]
    }

@router.get("/{ordine_id}", response_model=md.OrdineResponse)
def get_ordine(
    ordine_id: int, 
    db: Session = Depends(get_db),
    utente_id: int = Depends(get_utente_id_dal_token)
):
    ordine = cr.get_ordine_by_id(db, ordine_id)           
    
    if not ordine:
        raise HTTPException(status_code=404, detail=f"Ordine {ordine_id} non trovato")
    
    # Controllo di sicurezza: l'utente loggato può vedere solo il SUO ordine
    if ordine.get("utente_id") != utente_id:
        raise HTTPException(
            status_code=403, 
            detail="Non hai i permessi per visualizzare questo ordine"
        )
        
    return ordine

@router.patch("/{ordine_id}/stato", response_model=md.OrdineResponse)
def aggiorna_stato(ordine_id: int, nuovo_stato: md.StatoOrdine, db: Session = Depends(get_db)):
    # Nota: se vuoi che solo l'admin cambi lo stato, qui andrebbe 
    # aggiunta una verifica sul ruolo dell'utente loggato.
    ordine = cr.get_ordine_by_id(db, ordine_id)           
    
    if not ordine:
        raise HTTPException(status_code=404, detail=f"Ordine {ordine_id} non trovato")

    stato_corrente = ordine["stato"]
    stati_validi   = _TRANSIZIONI.get(stato_corrente, [])

    if nuovo_stato.value not in stati_validi:
        raise HTTPException(400, f"Transazione non valida {stato_corrente} -> {nuovo_stato.value}.")
    
    if nuovo_stato.value == "annullato":
        for riga in ordine["righe"]:
            prodotto = cr.get_prodotto_by_id(db, riga["prodotto_id"])
            if prodotto:
                cr.aggiorna_prodotto(
                    db,
                    riga["prodotto_id"],
                    {"stock": prodotto["stock"] + riga["quantita"]}
                )
    aggiornato = cr.aggiorna_stato_ordine(db, ordine_id, nuovo_stato.value)
    return aggiornato