from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

leituras = []
regando_manual = False
regando_auto = False

# Limiares para rega automática
TEMP_MAX = 32   # Temperatura máxima para ativar rega automática
HUM_MAX  = 70   # Humidade máxima para permitir rega automática

@app.route("/dados")
def dados():
    return jsonify({
        "leituras": leituras,
        "regando_manual": regando_manual,
        "regando_auto": regando_auto
    })

@app.route("/temperatura", methods=["POST"])
def temperatura():
    global leituras, regando_auto

    dados = request.get_json()
    temp = dados["temperatura"]
    hum  = dados["humidade"]

    # Adiciona leitura
    leituras.append({
        "temperatura": temp,
        "humidade": hum
    })
    if len(leituras) > 20:
        leituras.pop(0)

    # Rega automática
    if temp >= TEMP_MAX and hum < HUM_MAX:
        regando_auto = True
    else:
        regando_auto = False

    return jsonify({"ok": True})

# Rega manual
@app.route("/regar", methods=["POST"])
def regar():
    global regando_manual
    regando_manual = True
    return jsonify({"ok": True})

@app.route("/parar", methods=["POST"])
def parar():
    global regando_manual
    regando_manual = False
    return jsonify({"ok": True})

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    print("Servidor rodando...")
    app.run(host="0.0.0.0", port=5000)