# src/routes/routes_ordini.py

from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional
import modelli as md
import crud    as cr

router = APIRouter(
    prefix="/ordini",
    tags=["Ordini"]
)

@router.post("", response_model=md.OrdineResponse, status_code=status.HTTP_201_CREATED)
def crea_ordine(ordine: md.OrdineCreate):
    righe_elaborate = []
    totale          = 0.0
    prodotti_da_aggiornare = []

    # Verifica disponibilità per ogni riga
    for riga in ordine.righe:
        prodotto = cr.get_prodotto_per_id(riga.prodotto_id)

        if not prodotto:
            raise HTTPException(404, f"Prodotto {riga.prodotto_id} non trovato")

        if not prodotto.get("attivo") > 0:
            raise HTTPException(400, f"Prodotto '{prodotto['nome']}' non è disponibile")
        
        if prodotto["stock"] < riga.quantita:
            raise HTTPException(400, f"Stock insufficiente per '{prodotto['nome']}' "
                                f"disponibili {prodotto['stock']}, richiesti {riga.quantita}")
        
        subtotale = prodotto["prezzo"] * riga.quantita
        righe_elaborate.append({
            "prodotto_id":     riga.prodotto_id,
            "nome_prodotto":   prodotto["nome"],
            "prezzo_unitario": prodotto["prezzo"],
            "quantita":        riga.quantita,
            "subtotale":       round(subtotale, 2)
        })

        totale += subtotale
        prodotti_da_aggiornare.append({
            "id":          riga.prodotto_id,
            "nuovo_stock": prodotto["stock"] - riga.quantita
        })

        # Crea Ordine
        dati_ordine = {
            "cliente_nome":  ordine.cliente_nome,
            "cliente_email": ordine.cliente_email,
            "righe":         righe_elaborate,
            "totale":        round(totale, 2),
            "stato":         md.StatoOrdine.IN_ATTESA.value,
            "note":          ordine.note
        }

        nuovo_ordine = cr.crea_ordine(dati_ordine)

        # Aggiorniamo gli stock
        for p in prodotti_da_aggiornare:
            cr.aggiorna_prodotto(p["id"], {"stock": p["nuovo_stock"]})

        return nuovo_ordine

    @router.get("", response_model=dict)
    def get_ordini(
        stato: Optional[md.StatoOrdine] = None,
        email: Optional[str]            = None, 
        skip:  int                      = 0,
        limit: int                      = Query(10, ge=1, le=100)
    ):
        ordini = cr.get_tutti_ordini()

        if stato:
            ordini = [o for o in ordini if o["stato"] == stato.value]

        if email:
            ordini = [o for o in ordini if o["cliente_email"] == email]

        return {
            "totale": len(ordini),
            "ordini": ordini[skip: skip + limit]
        }

@router.get("/{ordine_id}", response_model=md.OrdineResponse)
def get_ordine(ordine_id: int):
    ordine = cr.get_ordine_by_id(ordine_id)           
    
    if not ordine:
        raise HTTPException(
            status_code=404,
            detail=f"Ordine {ordine_id} non trovato"
        )
    return ordine

@router.patch("/{ordine_id}/stato", response_model=md.OrdineResponse)
def aggiorna_stato(ordine_id: int, nuovo_stato: md.StatoOrdine):
    ordine = cr.get_ordine_by_id(ordine_id)           
    
    if not ordine:
        raise HTTPException(
            status_code=404,
            detail=f"Ordine {ordine_id} non trovato"
        )
    
    transizioni = {
        "in_attesa":  ["confermato", "annullato"],
        "confermato": ["spedito", "annullato"],
        "spedito":    ["consegnato"],
        "consegnato": [],
        "annullato":  []
    }

    stato_corrente = ordine["stato"]
    stati_validi   = transizioni.get(stato_corrente, [])

    if nuovo_stato.value not in stati_validi:
        raise HTTPException(400, f"Transazione non valida "
                            f"{stato_corrente} -> {nuovo_stato.value}. "
                            f"Transazioni valide: {stati_validi}")
    
    if nuovo_stato.value == "annullato":
        for riga in ordine["righe"]:
            prodotto = cr.get_prodotto_by_id(riga["prodotto_id"])
            if prodotto:
                cr.aggiorna_prodotto(
                    riga["prodotto_id"],
                    {"stock": prodotto["stock"] + riga["quantita"]}
                )
    aggiornato = cr.aggiorna_stato_ordine(ordine_id, nuovo_stato.value)
    return aggiornato            
