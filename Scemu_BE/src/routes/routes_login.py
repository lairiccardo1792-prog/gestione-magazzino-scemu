from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from src.modelli import utenti as md
from src.crud import crud_login as cr
from src.servizi.database import get_db
from src.servizi.token import crea_token_accesso  # <--- IMPORTA LA NUOVA FUNZIONE

# Rimuoviamo time e base64 perché non ci servono più per il token
router = APIRouter (
    prefix = "/login",
    tags= ["Autenticazione"]
)

@router.post("/", response_model=md.LoginResponse)
def login(dati : md.LoginRequest, db : Session = Depends(get_db)):
    # 1. La tua logica CRUD resta identica
    user_db = cr.verifica_passw(db, dati.user, dati.password)

    if not user_db: 
        return md.LoginResponse(success=False, message="Credenziali errate")

    # 2. SOSTITUIAMO la vecchia tokenizzazione Base64 con lo JWT professionale
    # Passiamo l'ID dell'utente che arriva dal tuo database (user_db.id)
    token_sicuro = crea_token_accesso(user_db.id)

    # 3. La risposta resta la stessa, cambia solo il "contenuto" del campo token
    return md.LoginResponse(
        success=True,
        message=f"Benvenuto {user_db.user}!",
        username=user_db.user,
        token=token_sicuro # <--- Ora questo è un vero JWT blindato
    )


