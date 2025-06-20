# PollingProg

## Descrizione
PollingProg è un'applicazione REST API per creare e partecipare a sondaggi.

## Funzionalità
- Lista e dettaglio sondaggi (accesso anonimo)
- Creazione, modifica e cancellazione sondaggi (utenti autenticati)
- Creazione scelte per sondaggi
- Votazione su sondaggi (1 voto per utente per sondaggio)
- Autenticazione con token JWT

## Come usare
1. Clonare il repository
2. Creare un ambiente virtuale e installare le dipendenze con `pip install -r requirements.txt`
3. Eseguire le migrazioni con `python manage.py migrate`
4. Avviare il server con `python manage.py runserver`
5. Usare il client Python o Postman per testare l'API

## Dipendenze principali
- Django
- djangorestframework
- djangorestframework-simplejwt
- requests (solo per il client Python)
