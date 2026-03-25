import random
import time
import requests

SERVIDOR = "http://192.168.43.1:5000"  # Coloque o IP do celular que está rodando o server

temp = 30.0
hum  = 40.0

print("Sensor iniciado...\n")

while True:
    try:
        estado = requests.get(SERVIDOR + "/dados").json()
        reg_manual = estado["regando_manual"]
        reg_auto   = estado["regando_auto"]

        # Regar se manual ou automático ativo
        if reg_manual or reg_auto:
            temp -= random.uniform(0.3, 0.7)
            hum  += random.uniform(1, 2)
        else:
            temp += random.uniform(-0.2, 0.5)
            hum  += random.uniform(-1, 1)

        temp = round(temp, 1)
        hum  = round(hum, 1)

        requests.post(SERVIDOR + "/temperatura", json={
            "temperatura": temp,
            "humidade": hum
        })

        print(f"Temp: {temp}°C | Hum: {hum}% | Regando Manual: {reg_manual} | Auto: {reg_auto}")

    except:
        print("Erro ao conectar ao servidor")

    time.sleep(3)