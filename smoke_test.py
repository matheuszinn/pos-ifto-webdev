import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def run_smoke_test():
    # Usar uma sessão para manter os cookies de autenticação
    session = requests.Session()
    
    print("--- 1. Registrando novo usuário ---")
    user_data = {"email": f"test_{int(time.time())}@agenda.com", "password": "securepassword"}
    r = session.post(f"{BASE_URL}/api/register", json=user_data)
    print(r.json())

    print("\n--- 2. Fazendo Login ---")
    r = session.post(f"{BASE_URL}/api/login", json=user_data)
    print(r.json())

    print("\n--- 3. Testando Agendamento via IA (Texto Livre) ---")
    prompt_data = {"prompt": "Tenho uma consulta médica amanhã às 09:00"}
    r = session.post(f"{BASE_URL}/api/ai/process", json=prompt_data)
    print(f"IA processou: {r.json().get('status')}")
    print(f"Evento criado: {r.json().get('event')}")

    print("\n--- 4. Gerando Rotina de Estudos de 3 dias via IA ---")
    routine_data = {
        "routine_type": "estudos de Python",
        "context": "estudar 2 horas por dia focado em Flask",
        "days": 3
    }
    r = session.post(f"{BASE_URL}/api/ai/routine", json=routine_data)
    print(f"Status da Rotina: {r.status_code}")
    print(f"IDs dos eventos gerados: {r.json().get('event_ids')}")

    print("\n--- 5. Listando todos os eventos na agenda ---")
    r = session.get(f"{BASE_URL}/api/events")
    events = r.json()
    print(f"Total de eventos encontrados: {len(events)}")
    for e in events:
        print(f" - [{e['start_time']}] {e['title']} (IA: {e['is_ai_generated']})")

if __name__ == "__main__":
    try:
        run_smoke_test()
    except requests.exceptions.ConnectionError:
        print("\nERRO: O servidor Flask não está rodando!")
        print("Abra outro terminal e execute: python3 -c 'from app import create_app; create_app().run()'")
