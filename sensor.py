"""
==============================================
  SENSOR IoT SIMULADO - Cliente HTTP
  Gera dados aleatórios e envia ao servidor
==============================================
"""

import random
import time
import requests
import argparse
from datetime import datetime

# ─── Configuração ───────────────────────────
SERVIDOR_URL = "http://localhost:5000/dados"

# Cada sensor tem: valor base, variação, e deriva lenta (simula mudança real)
SENSORES_CONFIG = {
    "temperatura": {"base": 25.0, "variacao": 0.8, "deriva": 0.05},
    "humidade":    {"base": 60.0, "variacao": 2.0, "deriva": 0.1},
    "pressao":     {"base": 1013.0, "variacao": 1.5, "deriva": 0.02},
    "luz":         {"base": 500.0, "variacao": 50.0, "deriva": 2.0},
}

LOCAIS = ["Sala A", "Sala B", "Exterior", "Laboratório", "Corredor"]


def gerar_valor(tipo, valor_atual, config):
    """Gera o próximo valor do sensor com variação realista."""
    # Deriva lenta (tendência)
    deriva = random.uniform(-config["deriva"], config["deriva"])
    # Variação aleatória (ruído)
    ruido = random.uniform(-config["variacao"], config["variacao"])
    novo_valor = valor_atual + deriva + ruido

    # Puxar de volta para a base se afastar muito (simula equilíbrio)
    diferenca = novo_valor - config["base"]
    novo_valor -= diferenca * 0.02  # Correção suave de 2%

    return round(novo_valor, 2)


def enviar_dado(sensor_id, tipo, valor, local):
    """Envia leitura ao servidor via HTTP POST."""
    payload = {
        "sensor_id": sensor_id,
        "tipo":      tipo,
        "valor":     valor,
        "local":     local,
    }
    try:
        resposta = requests.post(SERVIDOR_URL, json=payload, timeout=3)
        dados_resposta = resposta.json()

        alerta = dados_resposta.get("alerta", "normal")
        if alerta != "normal":
            print(f"  ⚠️  ALERTA recebido do servidor: valor {alerta}!")
        return True

    except requests.exceptions.ConnectionError:
        print("  ❌  Erro: Servidor não encontrado. Certifica-te que o server.py está a correr.")
        return False
    except Exception as e:
        print(f"  ❌  Erro ao enviar: {e}")
        return False


def simular_sensor(sensor_id, tipo, local, intervalo, total):
    """Loop principal do sensor."""
    config = SENSORES_CONFIG[tipo]
    valor_atual = config["base"]
    unidades = {"temperatura": "°C", "humidade": "%", "pressao": "hPa", "luz": "lux"}
    icones = {"temperatura": "🌡️", "humidade": "💧", "pressao": "🌬️", "luz": "☀️"}

    print(f"\n{'='*55}")
    print(f"  {icones[tipo]}  SENSOR IoT SIMULADO")
    print(f"{'='*55}")
    print(f"  ID:       {sensor_id}")
    print(f"  Tipo:     {tipo.capitalize()}")
    print(f"  Local:    {local}")
    print(f"  Destino:  {SERVIDOR_URL}")
    print(f"  Intervalo: {intervalo}s  |  Total: {'∞' if total == 0 else total} leituras")
    print(f"{'='*55}\n")

    contagem = 0
    try:
        while total == 0 or contagem < total:
            valor_atual = gerar_valor(tipo, valor_atual, config)
            timestamp = datetime.now().strftime("%H:%M:%S")

            print(f"[{timestamp}] 📤 Enviando → {tipo}: {valor_atual}{unidades[tipo]}", end=" ... ")
            sucesso = enviar_dado(sensor_id, tipo, valor_atual, local)

            if sucesso:
                print("✅ OK")
            contagem += 1
            time.sleep(intervalo)

    except KeyboardInterrupt:
        print(f"\n\n🛑  Sensor parado. Total de leituras enviadas: {contagem}")


def modo_multiplos_sensores(intervalo, total):
    """Simula vários sensores de forma sequencial (para demonstração simples)."""
    import threading

    sensores = [
        {"id": "SENSOR-T01", "tipo": "temperatura", "local": random.choice(LOCAIS)},
        {"id": "SENSOR-H01", "tipo": "humidade",    "local": random.choice(LOCAIS)},
        {"id": "SENSOR-P01", "tipo": "pressao",     "local": random.choice(LOCAIS)},
        {"id": "SENSOR-L01", "tipo": "luz",         "local": random.choice(LOCAIS)},
    ]

    valores_atuais = {s["id"]: SENSORES_CONFIG[s["tipo"]]["base"] for s in sensores}
    unidades = {"temperatura": "°C", "humidade": "%", "pressao": "hPa", "luz": "lux"}

    print(f"\n{'='*55}")
    print("  🌐  SIMULAÇÃO MULTI-SENSOR IoT")
    print(f"{'='*55}")
    for s in sensores:
        print(f"  📡  {s['id']} ({s['tipo']}) — {s['local']}")
    print(f"{'='*55}\n")

    contagem = 0
    try:
        while total == 0 or contagem < total:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"\n[{timestamp}] ── Ciclo {contagem + 1} ──────────────────")

            for s in sensores:
                config = SENSORES_CONFIG[s["tipo"]]
                novo_valor = gerar_valor(s["tipo"], valores_atuais[s["id"]], config)
                valores_atuais[s["id"]] = novo_valor

                print(f"  📤 {s['id']}: {novo_valor}{unidades[s['tipo']]}", end=" ... ")
                sucesso = enviar_dado(s["id"], s["tipo"], novo_valor, s["local"])
                print("✅" if sucesso else "❌")
                time.sleep(0.3)  # Pequeno delay entre sensores

            contagem += 1
            time.sleep(intervalo)

    except KeyboardInterrupt:
        print(f"\n\n🛑  Simulação parada. Ciclos completados: {contagem}")


# ─── Argumentos da linha de comandos ────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="🌡️  Simulador de Sensor IoT — envia dados ao servidor Flask"
    )
    parser.add_argument(
        "--tipo",
        choices=["temperatura", "humidade", "pressao", "luz", "todos"],
        default="todos",
        help="Tipo de sensor a simular (padrão: todos)",
    )
    parser.add_argument(
        "--id", default=None,
        help="ID do sensor (gerado automaticamente se omitido)",
    )
    parser.add_argument(
        "--local", default=None,
        help="Local do sensor (aleatório se omitido)",
    )
    parser.add_argument(
        "--intervalo", type=float, default=2.0,
        help="Segundos entre leituras (padrão: 2)",
    )
    parser.add_argument(
        "--total", type=int, default=0,
        help="Número total de leituras (0 = infinito)",
    )

    args = parser.parse_args()

    local = args.local or random.choice(LOCAIS)

    if args.tipo == "todos":
        modo_multiplos_sensores(args.intervalo, args.total)
    else:
        sensor_id = args.id or f"SENSOR-{args.tipo[:1].upper()}{random.randint(10,99)}"
        simular_sensor(sensor_id, args.tipo, local, args.intervalo, args.total)
