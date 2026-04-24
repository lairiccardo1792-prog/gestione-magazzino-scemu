# src/routes/routes_login.py

from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timedelta
import jwt
from src import modelli as md
from src import crud as cr

# Configurazione JWT
JWT_SECRET_KEY = "scemu-secret-key-2026"  # ⚠️ In produzione: usare variabile d'ambiente
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

router = APIRouter(
    tags=["Autenticazione"]
)

@router.post("/login", response_model=md.LoginResponse)
def login(credentials: md.LoginRequest):
    """
    Endpoint di login che autentica l'utente e ritorna un JWT token
    
    Args:
        credentials: LoginRequest con user e password
        
    Returns:
        LoginResponse con success, message, username, token
    """
    
    # 1. Validazione input
    if not credentials.user or not credentials.password:
        return md.LoginResponse(
            success=False,
            message="Username e password non possono essere vuoti",
            username=None,
            token=None
        )
    
    # 2. Verifica credenziali nel database
    if not cr.verify_password(credentials.user, credentials.password):
        return md.LoginResponse(
            success=False,
            message="Credenziali non valide",
            username=None,
            token=None
        )
    
    # 3. Recupera dati utente
    utente = cr.get_utente_by_username(credentials.user)
    if not utente:
        return md.LoginResponse(
            success=False,
            message="Utente non trovato",
            username=None,
            token=None
        )
    
    # 4. Genera JWT token
    payload = {
        "sub": utente["user"],  # subject = username
        "id": utente["id"],      # id utente
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)  # Scadenza
    }
    
    try:
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Errore nella generazione del token: {str(e)}"
        )
    
    # 5. Ritorna risposta di successo
    return md.LoginResponse(
        success=True,
        message="Accesso effettuato",
        username=utente["user"],
        token=token
    )
