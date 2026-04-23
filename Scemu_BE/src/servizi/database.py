# src/servizi/database.py

import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host":     "localhost",
    "port":     3306,
    "user":     "python",
    "password": "1234",
    "database": "ordini_base"
}

TABELLE_RICHIESTE = ["prodotti",
                     "ordini",
                     "righe_ordine"]

def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        raise RuntimeError ("Connessione a MariaDB fallita!")    
    
    cursore = conn.cursor()
    try:
        cursore.execute(
            "SELECT TABLE_NAME FROM information_schema.TABLES "
            "WHERE TABLE_SCHEMA = %s AND TABLE_NAME IN ({})".format(
                ", ".join(["%s"] * len(TABELLE_RICHIESTE))
            ), [DB_CONFIG["database"]] + TABELLE_RICHIESTE 
        )

        trovate = {row[0] for row in cursore.fetchall()}
        mancanti = set(TABELLE_RICHIESTE) - trovate

        if mancanti:
            conn.close()
            raise RuntimeError(
                f"Tabelle mancanti nel database '{DB_CONFIG['database']}' "
                f"{', '.join(sorted(mancanti))}"
            )
    finally:
        cursore.close()

    return conn        