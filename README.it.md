# SocialDex — Piattaforma Social con Certificazione Blockchain

🇬🇧 [Read in English](README.md)

Applicazione web full-stack sviluppata con Django che permette agli utenti di pubblicare post certificati automaticamente sulla blockchain Ethereum. Il contenuto di ogni post viene hashato con SHA-256, e l'hash viene scritto on-chain come payload di una transazione Ethereum — creando una prova permanente e immutabile dell'esistenza di quel contenuto in un dato momento.

## Funzionalità
- Registrazione e autenticazione utenti
- Monitoraggio IP: avvisa l'utente quando un login avviene da un IP diverso rispetto all'ultima sessione
- Certificazione automatica su blockchain alla creazione di un post
- Hash SHA-256 del contenuto, con il transaction ID risultante salvato insieme al post
- API REST JSON per tutti i post e per i post dell'ultima ora
- Ricerca full-text su titolo e contenuto dei post
- Pannello amministratore con conteggio post per utente
- Profilo utente pubblico con statistiche sui post
- Validazione base dei contenuti (filtro parole non consentite)
- Creazione automatica del profilo utente tramite Django signals

## Tecnologie utilizzate
- Python 3
- Django 3.1
- web3.py — integrazione con la blockchain Ethereum
- SHA-256 — hashing dei contenuti
- Ethereum Sepolia Testnet — certificazione on-chain
- SQLite
- Bootstrap 3, HTML/CSS

## Struttura del progetto
```
socialDex/     → configurazione del progetto Django
API/           → logica dei post, API REST, integrazione blockchain
  models.py    → modello Post (hash + transaction ID on-chain)
  views.py     → home, nuovo post, ricerca, post dell'ultima ora, API JSON
  utils.py     → invia la transazione di certificazione sulla blockchain
  wallet.py    → utility per generare un nuovo wallet Ethereum
accounts/      → autenticazione e gestione profilo utente
  models.py    → modello Profile (tracciamento IP)
  views.py     → register, login, logout
```

## Configurazione

1. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```
2. Copia `.env.example` in `.env` e inserisci i tuoi valori:
   ```bash
   cp .env.example .env
   ```
   - Genera una secret key Django:
     ```bash
     python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
     ```
   - Ottieni un endpoint RPC gratuito per Ethereum Sepolia da [Infura](https://www.infura.io/).
   - Genera un wallet per i test (non riutilizzare mai un wallet che detiene fondi reali):
     ```bash
     python API/wallet.py
     ```
   - Finanzia il wallet di test con ETH gratuiti su Sepolia tramite un [faucet pubblico](https://sepoliafaucet.com/) — necessario per pagare le gas fee delle transazioni on-chain.
3. Esegui le migrazioni e avvia il server:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser   # opzionale, per il pannello admin
   python manage.py runserver
   ```

## Note di sicurezza

- La secret key di Django e le credenziali blockchain (URL RPC, indirizzo wallet, chiave privata) **non sono mai** scritte direttamente nel codice: vengono caricate da un file `.env` locale, escluso dal controllo di versione tramite `.gitignore`.
- Anche `db.sqlite3` è escluso dal controllo di versione: contiene account utente reali (hash delle password) e contenuti — un file di database non dovrebbe mai essere caricato su un repository pubblico, indipendentemente dal suo contenuto.
- Se generi un wallet per questo progetto, tratta la sua chiave privata come sensibile anche su una testnet — non riutilizzarla per nulla che detenga valore reale.

## Note su questa versione

Questo progetto era originariamente basato sulla testnet **Ropsten** di Ethereum, deprecata definitivamente a fine 2022. Questa versione è stata aggiornata per usare **Sepolia**, l'attuale testnet Ethereum consigliata, e le chiamate a `web3.py` sono state aggiornate alla API moderna (v6+).

Durante la preparazione di questo repository per la pubblicazione, sono stati corretti anche alcuni problemi funzionali presenti nell'implementazione originale:
- Il passaggio di certificazione on-chain era definito nel modello `Post` ma non veniva mai effettivamente chiamato alla creazione di un nuovo post — i post venivano salvati ma mai certificati. Corretto chiamandolo esplicitamente dopo il salvataggio.
- Il campo `hash` era definito con `max_length=32`, troppo corto per un digest hex SHA-256 (64 caratteri). Corretto a 64.
- I metodi di validazione del filtro parole erano nominati in camelCase (`cleanTitle`/`cleanContent`), quindi il framework dei form di Django — che cerca `clean_<nomecampo>` — non li invocava mai. Rinominati in `clean_title`/`clean_content`, rendendo il filtro finalmente attivo.

## Scopo

Progetto personale realizzato per approfondire l'integrazione tra applicazioni web Django e la blockchain Ethereum, applicando concetti di immutabilità e certificazione digitale dei contenuti.
