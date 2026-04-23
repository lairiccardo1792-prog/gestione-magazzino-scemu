# src/servizi/modelli.py

from sqlalchemy import(
    Column, Integer, String, Float,
    Boolean, Text, DateTime, ForeignKey, func
)

from sqlalchemy.orm import relationship
from src.servizi.database import Base

# Prodotti
#*********
class ProdottiDB(Base):
    __tablename__ = "prodotti"

    id            = Column(Integer, primary_key=True, index=True)
    nome          = Column(String(500), nullable=False)
    descrizione   = Column(String(500), nullable=False)
    prezzo        = Column(Float, nullable=False)
    categoria     = Column(String(100), nullable=False)
    stock         = Column(Integer, default=0, nullable=False)
    attivo        = Column(Integer, default=1, nullable=False)
    creato_il     = Column(DateTime, server_default=func.now(), nullable=False)
    aggiornato_il = Column(DateTime, onupdate=func.now(), nullable=True)

    righe = relationship("RigaOrdineDB", back_populates="prodotto")

# Ordini
#*******
class OrdiniDB(Base):
    __tablename__ = "ordini"

    id            = Column(Integer, primary_key=True, index=True)
    utente_id     = Column(Integer, ForeignKey("utenti.id", ondelete="CASCADE"), nullable=False)
    cliente_nome  = Column(String(500), nullable=False)
    cliente_email = Column(String(500), nullable=False)
    totale        = Column(Float, nullable=False)
    stato         = Column(String(50), nullable=False, default="in_attesa")
    note          = Column(Text, nullable=False)
    creato_il     = Column(DateTime, server_default=func.now(), nullable=False)
    aggiornato_il = Column(DateTime, onupdate=func.now(), nullable=True)

    utente = relationship("UtentiDB", back_populates="ordini")

    righe = relationship("RigaOrdineDB", 
                         back_populates="ordine",
                         cascade="all, delete-orphan",
                         lazy="selectin")
    
# Righe Ordine
# #*************
# class RigaOrdineDB(Base):
#     __tablename__ = "righe_ordini"

#     id              = Column(Integer, primary_key=True, index=True)
#     ordine_id       = Column(Integer, ForeignKey("ordini.id", ondelete="CASCADE"), nullable=False)
#     prodotto_id     = Column(Integer, ForeignKey("prodotti.id"), nullable=False)
#     nome_prodotto   = Column(String(500), nullable=False)
#     prezzo_unitario = Column(Float, nullable=False)
#     quantita        = Column(Integer, nullable=False)
#     subtotale       = Column(Float, nullable=False)   

#     ordine   = relationship("OrdiniDB", back_populates="righe")
#     prodotto = relationship("ProdottiDB", back_populates="righe") 


class RigaOrdineDB(Base):
    __tablename__ = "righe_ordini" 

    id              = Column(Integer, primary_key=True, index=True)
    # Usiamo "ordini_id" come nel database
    ordini_id       = Column("ordini_id", Integer, ForeignKey("ordini.id", ondelete="CASCADE"), nullable=False)
    # Usiamo "prodotti_id" come nel database
    prodotti_id     = Column("prodotti_id", Integer, ForeignKey("prodotti.id"), nullable=False)
    
    nome_prodotto   = Column(String(500), nullable=False)
    prezzo_unitario = Column(Float, nullable=False)
    quantita        = Column(Integer, nullable=False)
    # Usiamo "sub_totale" come nel database
    subtotale       = Column("sub_totale", Float, nullable=False)   

    ordine   = relationship("OrdiniDB", back_populates="righe")
    prodotto = relationship("ProdottiDB", back_populates="righe")


class UtentiDB(Base):
    __tablename__ = 'utenti'  # Nome esatto della tabella in MySQL

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    

    ordini = relationship("OrdiniDB", back_populates="utente", cascade="all, delete-orphan")