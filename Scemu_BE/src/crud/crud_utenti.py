# src/crud/crud_utenti.py

from src.servizi.database import get_connection
from mysql.connector import Error

def get_utente_by_username(user: str):
    """
    Cerca un utente nel database per username
    
    Args:
        user: username da cercare
        
    Returns:
        dict con id, user, password oppure None se non trovato
    """
    conn = None
    try:
        conn = get_connection()
        cursore = conn.cursor(dictionary=True)
        
        query = "SELECT id, user, password FROM utenti WHERE user = %s"
        cursore.execute(query, (user,))
        
        risultato = cursore.fetchone()
        cursore.close()
        
        return risultato
        
    except Error as e:
        raise RuntimeError(f"Errore durante la ricerca dell'utente: {str(e)}")
    finally:
        if conn and conn.is_connected():
            conn.close()

def verify_password(user: str, password: str) -> bool:
    """
    Verifica se le credenziali sono corrette
    
    Args:
        user: username
        password: password da verificare (plaintext)
        
    Returns:
        True se credenziali valide, False altrimenti
    """
    utente = get_utente_by_username(user)
    
    if not utente:
        return False
    
    # Confronto plaintext (come da script SQL fornito)
    return utente.get("password") == password
