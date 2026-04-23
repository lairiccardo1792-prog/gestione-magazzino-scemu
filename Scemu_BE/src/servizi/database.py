# src/servizi/database.py

from sqlalchemy     import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from contextlib     import contextmanager
from typing         import Generator


# CONFIGURAZIONE
DB_CONFIG = {
    "host":     "localhost",
    "port":     3336,
    "user":     "Python",
    "password": "root",
    "database": "ordini_base"
}

DATABASE_URL = (
    "mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
).format(**DB_CONFIG)
TABELLE_RICHIESTE = {"prodotti", "ordini", "righe_ordini"}
# *********************************************************************

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    echo=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

# Base dichiarativa
class Base(DeclarativeBase):
    pass

# Context manager
@contextmanager
def get_session() -> Generator:
    session = SessionLocal()

    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()    

# Dipendenza FastAPI
def get_db():        
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()    

# Verifica tabelle all'avvio
def verifica_tabelle() -> None:        
    inspector = inspect(engine)

    tabelle_presenti = set(inspector.get_table_names())
    mancanti = TABELLE_RICHIESTE - tabelle_presenti

    if mancanti:
        raise RuntimeError("Database non coerente")