# src\crud\crud_login.py


from sqlalchemy.orm import Session
from sqlalchemy     import select
from src.servizi.modelli    import UtentiDB



def verifica_passw(db: Session ,user_input: str, password_input: str)  :
    user_db = db.query(UtentiDB).filter(UtentiDB.user == user_input).first()

    if not user_db:
        return None 
    
    if user_db.password == password_input:
        return user_db
    
    return False