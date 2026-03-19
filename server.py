"""
==============================================
  SERVIDOR IoT - Flask REST API
  Recebe dados de sensores simulados via HTTP
==============================================
"""

from flask import Flask, request, jsonify, render_template
from datetime import datetime
import json
import statistics

app = Flask(__name__)

# Armazenamento em memória dos dados recebidos
historico_dados = []

# Limites de alerta por tipo de sensor
LIMITES = {
    "temperatura": {"min": 15, "max": 35, "unidade": "°C"},
    "humidade":    {"min": 30, "max": 80, "unidade": "%"},
    "pressao":     {"min": 980, "max": 1030, "unidade": "hPa"},
    "luz":         {"min": 100, "max": 900, "unidade": "lux"},
}


def verificar_alerta(tipo, valor):
    """Verifica se o valor está fora dos limites normais."""
    if tipo not in LIMITES:
        return "normal"
    limites = LIMITES[tipo]
    if valor < limites["min"]:
        return "baixo"
    elif valor > limites["max"]:
        return "alto"
    return "normal"


# ─────────────────────────────────────────────────
#  ROTA: Receber dados do sensor (POST /dados)
# ─────────────────────────────────────────────────
@app.route("/dados", methods=["POST"])
def receber_dados():
    dados = request.get_json()

    if not dados or "sensor_id" not in dados or "tipo" not in dados or "valor" not in dados:
        return jsonify({"erro": "Dados inválidos. Campos obrigatórios: sensor_id, tipo, valor"}), 400

    timestamp = datetime.now().strftime("%H:%M:%S")
    tipo = dados["tipo"].lower()
    valor = float(dados["valor"])
    unidade = LIMITES.get(tipo, {}).get("unidade", "")
    alerta = verificar_alerta(tipo, valor)

    registro = {
        "sensor_id": dados["sensor_id"],
        "tipo":      tipo,
        "valor":     valor,
        "unidade":   unidade,
        "alerta":    alerta,
        "timestamp": timestamp,
        "local":     dados.get("local", "Desconhecido"),
    }

    historico_dados.append(registro)

    # Manter apenas os últimos 100 registros
    if len(historico_dados) > 100:
        historico_dados.pop(0)

    # Log no terminal com cor
    icones = {"temperatura": "🌡️", "humidade": "💧", "pressao": "🌬️", "luz": "☀️"}
    icone = icones.get(tipo, "📡")
    alerta_str = f" ⚠️  ALERTA: {alerta.upper()}" if alerta != "normal" else ""
    print(f"[{timestamp}] {icone}  Sensor {dados['sensor_id']} | {tipo.capitalize()}: {valor}{unidade} | {dados.get('local','')}{alerta_str}")

    return jsonify({"status": "ok", "alerta": alerta, "timestamp": timestamp}), 200


# ─────────────────────────────────────────────────
#  ROTA: Listar dados recebidos (GET /dados)
# ─────────────────────────────────────────────────
@app.route("/dados", methods=["GET"])
def listar_dados():
    tipo = request.args.get("tipo")
    sensor = request.args.get("sensor_id")
    ultimos = request.args.get("ultimos", 20, type=int)

    resultado = historico_dados[-ultimos:]

    if tipo:
        resultado = [d for d in resultado if d["tipo"] == tipo.lower()]
    if sensor:
        resultado = [d for d in resultado if d["sensor_id"] == sensor]

    return jsonify(resultado), 200


# ─────────────────────────────────────────────────
#  ROTA: Estatísticas (GET /estatisticas)
# ─────────────────────────────────────────────────
@app.route("/estatisticas", methods=["GET"])
def estatisticas():
    if not historico_dados:
        return jsonify({"mensagem": "Sem dados ainda"}), 200

    stats = {}
    tipos = set(d["tipo"] for d in historico_dados)

    for tipo in tipos:
        valores = [d["valor"] for d in historico_dados if d["tipo"] == tipo]
        alertas = [d for d in historico_dados if d["tipo"] == tipo and d["alerta"] != "normal"]
        unidade = LIMITES.get(tipo, {}).get("unidade", "")
        stats[tipo] = {
            "total_leituras": len(valores),
            "media":  round(statistics.mean(valores), 2),
            "minimo": round(min(valores), 2),
            "maximo": round(max(valores), 2),
            "desvio_padrao": round(statistics.stdev(valores), 2) if len(valores) > 1 else 0,
            "total_alertas": len(alertas),
            "unidade": unidade,
        }

    return jsonify(stats), 200


# ─────────────────────────────────────────────────
#  ROTA: Dashboard HTML (GET /)
# ─────────────────────────────────────────────────
@app.route("/")
def dashboard():
    return render_template("dashboard.html")


# ─────────────────────────────────────────────────
#  ROTA: Limpar dados (DELETE /dados)
# ─────────────────────────────────────────────────
@app.route("/dados", methods=["DELETE"])
def limpar_dados():
    historico_dados.clear()
    print("🗑️  Histórico de dados limpo.")
    return jsonify({"status": "ok", "mensagem": "Dados limpos com sucesso"}), 200


if __name__ == "__main__":
    print("=" * 55)
    print("  🌐  SERVIDOR IoT INICIADO")
    print("=" * 55)
    print("  Dashboard: http://localhost:5000")
    print("  API POST:  http://localhost:5000/dados")
    print("  API GET:   http://localhost:5000/dados")
    print("  Stats:     http://localhost:5000/estatisticas")
    print("=" * 55)
    app.run(debug=True, port=5000)
