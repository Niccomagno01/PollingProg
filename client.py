import requests

API_URL = "http://127.0.0.1:8000/api"
USERNAME = "admin"
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
    choice_id = new_poll['choices'][0]['id']  # voto per la prima scelta
    vote_result = vote_poll(access_token, poll_id, choice_id)
    print("Voto registrato:", vote_result)
