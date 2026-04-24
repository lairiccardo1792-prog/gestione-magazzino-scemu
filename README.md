# 🥊 Gestione Magazzino - Scemu - Televideocom . Co

## 📸 Anteprima Progetto
Qui sotto puoi vedere l'interfaccia del gestionale in azione:

### 📊 Dashboard Analisi e Statistiche
(TRASCINA QUI LA TUA FOTO Immagine_progetto.png)

### 📦 Gestione Magazzino e Scorte
(TRASCINA QUI LA TUA FOTO lista_prodotti.png)

### 🛒 Gestione Ordini e Clienti
(TRASCINA QUI LA TUA FOTO Crea_Ordine.png)

---

## 🏗️ Architettura del Progetto
Il sistema è diviso in due macro-aree principali per garantire scalabilità e pulizia del codice.

### 🐍 Backend (`Scemu_BE`)
Costruito con un'architettura moderna in Python, focalizzata su velocità e sicurezza.
- **Framework:** **FastAPI** per la creazione di API REST rapide e documentate automaticamente.
- **ORM:** **SQLAlchemy** per la gestione del database tramite modelli Python.
- **Validazione Dati:** **Pydantic** per assicurare che ogni dato in ingresso sia corretto prima di essere elaborato.
- **Database:** **MariaDB** (Script disponibile nella cartella `/Database`).
- **Operazioni:** Implementazione completa di rotte **CRUD** per la gestione di ordini, prodotti e utenti.

### 🅰️ Frontend (`Scemu_FE`)
Un'interfaccia reattiva e dinamica che comunica in tempo reale con le API del backend.
- **Framework:** **Angular 17+**.
- **Logica:** Sviluppata in **TypeScript (TS)** per un codice robusto e tipizzato.
- **Struttura:** HTML5 semantico e **CSS3** personalizzato per un'interfaccia moderna e "abbellita".

---

## 💾 Schema del Database
Il database `ordini_base` gestisce le seguenti entità principali:
- **Utenti**, **Prodotti**, **Ordini**, **Righe Ordini**.
> 📄 Trovi lo script completo qui: [db.sql](./Database/db.sql)

---

## 🛠️ Technologies Used
- **Python:** Pandas, SQLAlchemy, Pydantic, Uvicorn, PyJWT, FastAPI
- **SQL:** MariaDB
- **Frontend:** Angular, TypeScript, CSS3
- **Version Control:** GitHub

---

## 🚀 Come avviare il progetto

### Backend
1. `cd Scemu_BE`
2. `pip install fastapi sqlalchemy pydantic uvicorn pyjwt pandas`
3. `uvicorn main:app --reload`

### Frontend
1. `cd Scemu_FE`
2. `npm install`
3. `ng serve`

---

## ✍️ Authors
* **Riccardo Lai**
* **Alessio Pilloni**
* **Federico Asunis**
Perché è meglio così?