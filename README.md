# PollingProg

**PollingProg** è un'applicazione web per creare e gestire sondaggi online.  
Gli utenti possono registrarsi, creare sondaggi con più scelte, votare e visualizzare i risultati.  
L'app utilizza **Django REST Framework** per l'API backend, con autenticazione **JWT**.

---

## 🌐 Link al sito

Il progetto è ospitato su **Railway**:  
🔗 [https://web-production-e349a.up.railway.app](https://web-production-e349a.up.railway.app)

---

## 🚀 Funzionalità principali

- Registrazione e autenticazione utenti con JWT
- Creazione, modifica e cancellazione di sondaggi (solo da parte del creatore o admin)
- Aggiunta di scelte a ciascun sondaggio
- Votazione ai sondaggi da parte degli utenti autenticati
- Visualizzazione dei risultati con conteggio voti per ogni scelta
- Endpoint protetti da permessi e autenticazione

---

## 🔐 API Endpoints principali

| Metodo | Endpoint                         | Descrizione                           | Accesso                   |
|--------|----------------------------------|---------------------------------------|---------------------------|
| POST   | `/api/accounts/register/`        | Registrazione nuovo utente            | Pubblico                  |
| POST   | `/api/token/`                    | Login e ottenimento token JWT         | Pubblico                  |
| GET    | `/api/polls/`                    | Lista sondaggi                        | Anonimi e autenticati     |
| POST   | `/api/polls/`                    | Creazione sondaggio                   | Solo utenti autenticati   |
| GET    | `/api/polls/<poll_id>/`          | Dettagli sondaggio                    | Anonimi e autenticati     |
| PUT    | `/api/polls/<poll_id>/`          | Aggiornamento sondaggio               | Solo creatore o admin     |
| POST   | `/api/polls/<poll_id>/vote/`     | Votazione                              | Solo utenti autenticati   |
| POST   | `/api/polls/<poll_id>/choices/`  | Aggiunta scelta a sondaggio           | Solo creatore o admin     |
| GET    | `/api/accounts/me/`              | Informazioni utente autenticato       | Solo autenticati          |

---

## 🖥️ Descrizione del sito

Questo sito permette agli utenti di:
- Registrarsi e autenticarsi
- Creare nuovi sondaggi con domande personalizzate
- Aggiungere scelte ai sondaggi
- Votare nei sondaggi esistenti
- Visualizzare i risultati in tempo reale

> ℹ️ **Nota:** per modificare un sondaggio, è necessario cliccare il tasto **"Modifica"** nella pagina del sondaggio e scorrere in alto.

---

## 👤 Utenti di test predefiniti

| Username | Password     |
|----------|--------------|
| admin    | 123456789    |
| user     | qwertyuiop   |
| user3    | 1234         |
| user4    | asdf         |
| user5    | qwer         |




