import requests
import random
import time
from datetime import datetime

API_URL = "http://localhost:8000/energia"   # Altere para a URL da API quando publicar

usuarios = [f"USR-{i:02d}" for i in range(1, 11)]

while True:
    usuario = random.choice(usuarios)
    payload = {
        "usuario": usuario,
        "geracao_kwh": round(random.uniform(5, 25), 2),
        "consumo_kwh": round(random.uniform(2, 10), 2),
        "timestamp": datetime.utcnow().isoformat()
    }
    try:
        resp = requests.post(API_URL, json=payload)
        print(f"Enviado {usuario}: {resp.json()}")
    except Exception as e:
        print(f"Erro: {e}")
    time.sleep(5)