"""
Servidor - recebe temperatura e serve o dashboard
"""
from flask import Flask, jsonify, request, render_template
from datetime import datetime

app = Flask(__name__)

leituras = []

@app.route("/temperatura", methods=["POST"])
def receber():
    dados  = request.get_json()
    valor  = dados["valor"]
    hora   = datetime.now().strftime("%H:%M:%S")

    leituras.append({"valor": valor, "hora": hora})

    if len(leituras) > 20:
        leituras.pop(0)

    print(f"[{hora}] Temperatura: {valor}°C")
    return jsonify({"ok": True})


@app.route("/dados")
def dados():
    return jsonify(leituras)


@app.route("/")
def pagina():
    return render_template("index.html")


if __name__ == "__main__":
    print("Servidor a correr em http://localhost:5000")
    app.run(debug=True, port=5000)