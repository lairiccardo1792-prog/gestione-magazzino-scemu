# src/main.py

from fastapi        import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from collections    import Counter
from contextlib     import asynccontextmanager
import time

import routes.routes_ordini as rt_ordini 
import routes.routes_prodotti as rt_prodotti # <--- Assicurati che il percorso sia corretto
import routes.routes_login as rt_login
import crud as cr
from servizi.database import get_db, verifica_tabelle

@asynccontextmanager
async def lifespan(app: FastAPI):
    verifica_tabelle()
    yield

app=FastAPI(
    title       = "SCEMU Negozio Online",
    description = "API per la gestione di un negozio online",
    version     = "1.0.0",
    lifespan    = lifespan  
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200","http://127.0.0.1:4200"], # Permetti ad Angular
    allow_credentials=True,
    allow_methods=["*"], # Permetti tutti i metodi (GET, POST, etc.)
    allow_headers=["*"], # Permetti tutti gli header
)
@app.middleware("http")
async def aggiungi_tempo_risposta(request, call_next):
    inizio = time.time()
    risposta = await call_next(request)
    durata = time.time() - inizio
    risposta.headers["X-Process-Time"] = str(round(durata, 4))
    
    return risposta

app.include_router(rt_ordini.router)
app.include_router(rt_prodotti.router)
app.include_router(rt_login.router)

@app.get("/", tags=["Info"])
def root():
    return {
        "api":         "SCEMU Negozio Online",
        "description": "API per la gestione di un negozio online",
        "version":     "1.0.0",
        "documentat":  "/docs",
        "storage":     "MariaDB"    
    }

@app.get("/statistiche", tags=["Info"])
def statistiche(db: Session = Depends(get_db)):
    tt_prodotti = cr.get_tutti_prodotti(db)
    tt_ordini   = cr.get_tutti_ordini(db)

    if not tt_prodotti and not tt_ordini:
        return {"messaggio": "Nessun dato disponibile"}
    
    pr_attivi  = [p for p in tt_prodotti if p.get("attivo", 0) > 0]
    stk_totale = sum(p.get("stock", 0) for p in tt_prodotti)
    valore_mgz = sum(p.get("prezzo", 0) * p.get("stock", 0) for p in tt_prodotti)

    ord_per_stato  = Counter(o["stato"] for o in tt_ordini)
    ord_completati = [o for o in tt_ordini if o["stato"] == "consegnato"]
    fatturato_tot  = sum(o["totale"] for o in ord_completati)
    media_ordine   = (fatturato_tot / len(ord_completati) if ord_completati else 0)
    
    # --- CORREZIONE VENDITE PER PRODOTTO (Evita TypeError) ---
    vendite_per_prodotto = Counter()
    for ordine in ord_completati:
        for riga in ordine.get("righe", []):
            # Usiamo int() perché se arriva dal DB come stringa, Python crasha al +=
            nome_p = riga.get("nome_prodotto", "Ignoto")
            qty_p = int(riga.get("quantita", 0)) 
            vendite_per_prodotto[nome_p] += qty_p

    top_prodotti = vendite_per_prodotto.most_common(5)

    # --- CORREZIONE VENDITE PER CATEGORIA (Logica corretta) ---
    categorie_per_prodotto = {p["nome"]: p.get("categoria", "Altro") for p in tt_prodotti}
    vendite_per_categoria  = Counter()
    
    # Cicliamo sulle vendite effettive, non sul catalogo prodotti
    for nome, quantita in vendite_per_prodotto.items():
        cat = categorie_per_prodotto.get(nome, "Altro")
        vendite_per_categoria[cat] += quantita

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