# 🌐 Sistema IoT Simulado — Python

Projeto educativo que simula uma arquitetura IoT completa:
**Sensor → HTTP → Servidor (API REST) → Dashboard Web**

---

## 📁 Estrutura de Ficheiros

```
iot_simulator/
├── server.py            ← Servidor Flask (API REST + Dashboard)
├── sensor.py            ← Simulador de sensor(es) IoT
├── requirements.txt     ← Dependências Python
└── templates/
    └── dashboard.html   ← Interface web do dashboard
```

---

## ⚙️ Instalação

```bash
pip install -r requirements.txt
```

---

## 🚀 Como Executar

### 1. Inicia o Servidor (Terminal 1)
```bash
python server.py
```
Abre o browser em: **http://localhost:5000**

### 2. Inicia o(s) Sensor(es) (Terminal 2)

**Todos os sensores ao mesmo tempo:**
```bash
python sensor.py
```

**Sensor específico:**
```bash
python sensor.py --tipo temperatura
python sensor.py --tipo humidade
python sensor.py --tipo pressao
python sensor.py --tipo luz
```

**Opções avançadas:**
```bash
python sensor.py --tipo temperatura --id SENSOR-T99 --local "Sala C" --intervalo 1 --total 50
```

| Argumento    | Descrição                              | Padrão |
|-------------|----------------------------------------|--------|
| `--tipo`    | temperatura / humidade / pressao / luz / todos | todos  |
| `--id`      | ID do sensor                          | Aleatório |
| `--local`   | Nome do local                         | Aleatório |
| `--intervalo`| Segundos entre leituras              | 2.0    |
| `--total`   | Número de leituras (0 = infinito)     | 0      |

---

## 🌐 Endpoints da API

| Método | Rota              | Descrição                        |
|--------|-------------------|----------------------------------|
| GET    | `/`               | Dashboard Web                    |
| POST   | `/dados`          | Enviar leitura de sensor         |
| GET    | `/dados`          | Listar leituras recentes         |
| GET    | `/estatisticas`   | Estatísticas por tipo de sensor  |
| DELETE | `/dados`          | Limpar todos os dados            |

### Formato do POST /dados
```json
{
  "sensor_id": "SENSOR-T01",
  "tipo": "temperatura",
  "valor": 24.5,
  "local": "Sala A"
}
```

---

## 🏗️ Arquitetura IoT Demonstrada

```
┌─────────────────┐    HTTP POST    ┌──────────────────────┐
│   sensor.py     │ ─────────────→  │     server.py        │
│                 │                 │                      │
│  • Gera valores │                 │  • Recebe dados      │
│  • Simula ruído │                 │  • Verifica alertas  │
│  • Envia via    │                 │  • Armazena em RAM   │
│    HTTP REST    │                 │  • Calcula stats     │
└─────────────────┘                 │  • Serve Dashboard   │
                                    └──────────┬───────────┘
                                               │
                                    ┌──────────▼───────────┐
                                    │   Browser (GET /)    │
                                    │   Dashboard em tempo │
                                    │   real (atualiza 3s) │
                                    └──────────────────────┘
```

---

## 📡 Tipos de Sensores e Limites

| Sensor       | Normal       | Unidade |
|-------------|--------------|---------|
| Temperatura  | 15°C – 35°C  | °C      |
| Humidade     | 30% – 80%    | %       |
| Pressão      | 980 – 1030   | hPa     |
| Luminosidade | 100 – 900    | lux     |

Valores fora destes limites geram **alertas** no dashboard.

---

## 🧠 Conceitos IoT Abordados

- **Dispositivo/Sensor**: `sensor.py` — gera e envia dados
- **Protocolo de comunicação**: HTTP REST (POST/GET)
- **Servidor/Cloud local**: Flask API com armazenamento em memória
- **Dashboard**: Interface web com atualização em tempo real
- **Alertas**: Deteção automática de valores anómalos
- **Escalabilidade**: Múltiplos sensores simultâneos
