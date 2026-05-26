import requests
import random
import time
from datetime import datetime

# ⚠️ ALTERE ESTA URL PARA A URL DA SUA API APÓS O DEPLOY NO RENDER
API_URL = "http://localhost:8000/energia"   # ou "https://suer-api.onrender.com/energia"

usuarios = [f"USR-{i:02d}" for i in range(1, 11)]

print(f"Simulador iniciado. Enviando para {API_URL}")

while True:
    usuario = random.choice(usuarios)
    payload = {
        "usuario": usuario,
        "geracao_kwh": round(random.uniform(5, 25), 2),
        "consumo_kwh": round(random.uniform(2, 10), 2),
        "timestamp": datetime.utcnow().isoformat()
    }
    try:
        resp = requests.post(API_URL, json=payload, timeout=5)
        if resp.status_code == 200:
            print(f"✓ {usuario} | Enviado: {payload} | Resposta: {resp.json()}")
        else:
            print(f"✗ Erro HTTP {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"✗ Falha ao enviar: {e}")
    time.sleep(5)