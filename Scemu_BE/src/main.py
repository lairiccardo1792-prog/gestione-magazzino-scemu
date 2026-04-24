# src/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from collections import Counter
import time

from src.routes import routes_ordini as ordini
from src.routes import routes_prodotti as prodotti
from src.routes import routes_login as login
from src import crud as cr
app=FastAPI(
    title="SCEMU Negozio Online",
    description="API per la gestione di un negozio online",
    version="1.0.0"  
)

"""
    allow_origin=[
        "http://localhost:3000",
        "https://miosito.com"
    ]
    """
app.add_middleware(
    CORSMiddleware,    
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"], #vale sempre *
    allow_headers=["*"]
)

@app.middleware("http")
async def aggiungi_tempo_risposta(request, call_next):
    inizio = time.time()
    risposta = await call_next(request)
    durata = time.time() - inizio
    risposta.headers["X-Process-Time"] = str(round(durata, 4))
    
    return risposta

app.include_router(login.router)
app.include_router(ordini.router)
app.include_router(prodotti.router)

app.get("/", tags=["Info"])
def root():
    return {
        "api":         "SCEMU Negozio Online",
        "description": "API per la gestione di un negozio online",
        "version":     "1.0.0",
        "documentat":  "/docs",
        "storage":     "MariaDB"    
    }

@app.get("/statistiche", tags=["Info"])
def statistiche():
    tt_prodotti = cr.get_tutti_prodotti()
    tt_ordini   = cr.get_tutti_ordini()

    if not tt_prodotti and not tt_ordini:
        return {"messaggio": "Nessun dato disponibile"}
    
    pr_attivi  = [p for p in tt_prodotti if p.get("attivo") > 0]
    stk_totale = sum(p["stock"] for p in tt_prodotti)
    valore_mgz = sum(p["prezzo"] * p["stock"] for p in tt_prodotti)

    ord_per_stato  = Counter(o["stato"] for o in tt_ordini)
    ord_completati = [o for o in tt_ordini if o["stato"]=="consegnato"]
    fatturato_tot  = sum(o["totale"] for o in ord_completati)
    media_ordine   = (fatturato_tot / len(ord_completati) if ord_completati else 0)
    
    vendite_per_prodotto = Counter()
    for ordine in ord_completati:
        for riga in ordine["righe"]:
            vendite_per_prodotto[riga["nome_prodotto"]] += riga["quantita"]

    top_prodotti = vendite_per_prodotto.most_common(5)

    categorie_per_prodotto = {p["nome"]: p["categoria"] for p in tt_prodotti}
    vendite_per_categoria  = Counter()
    for ordine in ord_completati:
        for riga in ordine["righe"]:
            nome_prodotto = riga["nome_prodotto"]
            cat = categorie_per_prodotto.get(nome_prodotto, "Altro")
            vendite_per_categoria[cat] += riga["quantita"]

    return {
        "prodotti": {
            "totale":        len(tt_prodotti),
            "attivi":        len(pr_attivi),
            "stock_totale":  stk_totale,
            "val_magazzino": round(valore_mgz, 2)
        },
        "ordini": {
            "totale":        len(tt_ordini),
            "per_stato":     dict(ord_per_stato),
            "fatt_totale":   round(fatturato_tot, 2),
            "media_ordine":  round(media_ordine, 2)
        },
        "top_prodotti": [
            {"prodotto": nome, "unita_vendute": qty} for nome, qty in top_prodotti
        ],
        "vendite_per_categoria": dict(vendite_per_categoria)
    }           