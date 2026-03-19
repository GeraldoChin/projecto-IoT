"""
Sensor de temperatura - gera valores e envia ao servidor
"""
import random
import time
import requests

SERVIDOR = "http://localhost:5000/temperatura"

temperatura = 25.0

print("Sensor iniciado! A enviar dados a cada 2 segundos...")
print("Ctrl+C para parar\n")

while True:
    temperatura += random.uniform(-0.5, 0.5)
    temperatura  = round(temperatura, 1)

    try:
        requests.post(SERVIDOR, json={"valor": temperatura})
        print(f"Enviado: {temperatura}°C")
    except:
        print("Erro: servidor não encontrado. Inicia o server.py primeiro.")

    time.sleep(10)