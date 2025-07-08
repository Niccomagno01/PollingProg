

# client.py
import requests

API_URL = "http://127.0.0.1:8000/api"
USERNAME = "admin" # Assicurati che questo utente sia un superuser o il creatore del poll
PASSWORD = "123456789"

def get_tokens(username, password):
    url = f"{API_URL}/token/"
    response = requests.post(url, json={"username": username, "password": password})
    response.raise_for_status()
    return response.json()

def list_polls(access_token):
    url = f"{API_URL}/polls/"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def create_poll(access_token, question, choices):
    url = f"{API_URL}/polls/"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "question": question,
        "choices": [{"choice_text": c} for c in choices]
    }
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()

def vote_poll(access_token, poll_id, choice_id):
    url = f"{API_URL}/polls/{poll_id}/vote/"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"choice": choice_id}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()

def update_poll(access_token, poll_id, question=None, choices=None):
    url = f"{API_URL}/polls/{poll_id}/"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    data = {}
    if question:
        data["question"] = question
    if choices is not None: # Permette di passare una lista vuota per rimuovere tutte le choices
        data["choices"] = [{"choice_text": c} for c in choices]

    response = requests.put(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    # Login e ottieni token
    tokens = get_tokens(USERNAME, PASSWORD)
    access_token = tokens['access']
    print("Access token ottenuto")

    # Lista polls
    polls = list_polls(access_token)
    print("Polls attuali:", polls)

    # Crea un poll nuovo (esempio)
    question = "Qual è il tuo colore preferito?"
    choices = ["Rosso", "Blu", "Verde"]
    new_poll = create_poll(access_token, question, choices)
    print("Poll creato:", new_poll)

    # Vota al poll (prendi poll_id e choice_id dal poll creato)
    poll_id = new_poll['id']
    if new_poll['choices']: # Assicurati che ci siano choices prima di votare
        choice_id = new_poll['choices'][0]['id']  # voto per la prima scelta
        vote_result = vote_poll(access_token, poll_id, choice_id)
        print("Voto registrato:", vote_result)
    else:
        print("Nessuna scelta disponibile per votare nel nuovo sondaggio.")

    # Esempio di aggiornamento di un poll esistente
    print("\n--- Tentativo di aggiornare il poll ---")
    try:
        updated_question = "Qual è il tuo animale preferito?"
        updated_choices = ["Cane", "Gatto", "Uccello", "Pesce"]
        # Usa il poll_id del sondaggio appena creato
        updated_poll = update_poll(access_token, poll_id, question=updated_question, choices=updated_choices)
        print("Poll aggiornato:", updated_poll)
    except requests.exceptions.HTTPError as e:
        print(f"Errore nell'aggiornamento del poll: {e.response.status_code} - {e.response.text}")

    print("\n--- Tentativo di aggiornare il poll (solo domanda) ---")
    try:
        updated_question_only = "Qual è il tuo hobby preferito?"
        updated_poll_q_only = update_poll(access_token, poll_id, question=updated_question_only)
        print("Poll aggiornato (solo domanda):", updated_poll_q_only)
    except requests.exceptions.HTTPError as e:
        print(f"Errore nell'aggiornamento del poll (solo domanda): {e.response.status_code} - {e.response.text}")

    print("\n--- Tentativo di aggiornare il poll (solo choices) ---")
    try:
        updated_choices_only = ["Lettura", "Sport", "Musica"]
        updated_poll_c_only = update_poll(access_token, poll_id, choices=updated_choices_only)
        print("Poll aggiornato (solo choices):", updated_poll_c_only)
    except requests.exceptions.HTTPError as e:
        print(f"Errore nell'aggiornamento del poll (solo choices): {e.response.status_code} - {e.response.text}")