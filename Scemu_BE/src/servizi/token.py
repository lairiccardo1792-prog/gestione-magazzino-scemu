import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Il tuo "sigillo" segreto. 
# Importante: in un progetto reale questa stringa starebbe in un file .env
SECRET_KEY = "la_tua_chiave_segreta_molto_difficile_da_indovinare"
ALGORITHM = "HS256"

# Questo oggetto serve a FastAPI per capire che deve cercare 
# un'intestazione "Authorization: Bearer <token>"
security = HTTPBearer()

def crea_token_accesso(utente_id: int):
    """
    FASE 1: EMISSIONE
    Prende l'ID che hai appena trovato nel DB dopo il login e lo mette nel token.
    """
    # Impostiamo la scadenza a 24 ore da questo momento
    scadenza = datetime.utcnow() + timedelta(hours=24)
    
    # Il "Payload" è il contenuto del pacchetto
    payload = {
        "sub": str(utente_id),  # Salviamo l'ID come stringa (standard JWT)
        "exp": scadenza         # Aggiungiamo la data di scadenza
    }
    
    # Firmiamo il tutto e otteniamo la stringa criptata
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_utente_id_dal_token(auth: HTTPAuthorizationCredentials = Security(security)):
    """
    FASE 2: RECUPERO (Il "Poliziotto alla dogana")
    Estrae l'ID dal token ogni volta che l'utente fa una richiesta (es. ordini).
    """
    try:
        # Proviamo a decodificare il token con la nostra chiave segreta
        payload = jwt.decode(auth.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Estraiamo l'ID (il campo 'sub')
        utente_id: str = payload.get("sub")
        
        if utente_id is None:
            raise HTTPException(status_code=401, detail="Token non valido: ID mancante")
            
        # Ritorniamo l'ID convertito in numero, pronto per essere usato nelle query SQL
        return int(utente_id)
        
    except jwt.ExpiredSignatureError:
        # Se sono passate più di 24 ore...
        raise HTTPException(status_code=401, detail="Il token è scaduto. Per favore, rifai il login.")
    except jwt.PyJWTError:
        # Se il token è stato manomesso o è scritto male...
        raise HTTPException(status_code=401, detail="Token non valido o corrotto")