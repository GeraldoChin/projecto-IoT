# 🌐 Sistema IoT Simulado — Python

Projeto educativo que simula uma arquitetura IoT completa:
**Sensor → HTTP → Servidor (API REST) → Dashboard Web**


##  Instalação


pip install -r requirements.txt

#  Sistema IoT de Irrigação Inteligente - Simulação

## 1. Problema

Em ambientes agrícolas, a irrigação inadequada pode causar prejuízos:  
- Regar demais pode danificar plantas e aumentar desperdício de água.  
- Regar de menos prejudica o crescimento e a produção.  

Além disso, o monitoramento manual da temperatura e humidade exige esforço constante.  
Este projeto simula um **sistema de irrigação inteligente**, que:  
- Monitora temperatura e humidade do ambiente em tempo real.  
- Aciona irrigação automaticamente se a temperatura estiver alta e a humidade baixa.  
- Permite controle manual via dashboard.  
- Fornece visualização em tempo real através de uma webcam simulada.


## 2. Objetivo da Simulação

- Criar uma **simulação realista de um sistema IoT agrícola** usando apenas smartphones e um PC.  
- Demonstrar a integração entre sensores, atuadores, dispositivos edge e dashboard web.  
- Fornecer gráficos em tempo real para monitoramento visual e dados históricos.



 3. Estrutura do Projeto


iot_irrigacao/
├── server.py           # Servidor Flask (API + dashboard)
├── sensor.py           # Simulador de sensores de temperatura e humidade
├── requirements.txt    # Dependências Python
└── templates/
    └── index.html      # Dashboard web com gráfico, botões e webcam


4. Tecnologias Utilizadas

* Python 3
* Flask (API REST + servidor web)
* Requests (comunicação HTTP sensor → servidor)
* Chart.js (gráfico em tempo real no dashboard)
* Navegador web para dashboard
* IP Webcam (app Android) para simulação de câmera

---

 5. Funcionamento

1. Servidor (Celular 1):

   * Roda `server.py`.
   * Recebe leituras de temperatura e humidade do sensor via HTTP POST.
   * Processa lógica de rega automática com base em limiares definidos:

     * **Temperatura ≥ 32°C** e **Humidade < 70%** → aciona rega automática.
   * Exibe dashboard web com gráficos, status de rega e webcam.

2. **Sensor (Celular 2)**:

   * Roda `sensor.py`.
   * Simula leitura de temperatura e humidade.
   * Se rega (manual ou automática) estiver ativa:

     * Temperatura diminui.
     * Humidade aumenta.
   * Envia dados para o servidor a cada 3 segundos.

3. **Dashboard (PC ou outro dispositivo)**:

   * Acessa via navegador `http://IP_DO_SERVIDOR:5000`.
   * Mostra:

     * Valores atuais de temperatura e humidade.
     * Gráfico histórico em tempo real.
     * Botões para rega manual.
     * Status do sistema (manual, automático ou parado).
     * Stream da webcam para monitoramento visual.

---

## 6. Simulação Realista

* **Regra lógica aplicada**: rega automática só ocorre quando temperatura está alta **e humidade não está acima do limite**, evitando regar em excesso.
* **Rega manual**: pode ser ativada a qualquer momento pelo usuário.
* **Dashboard interativo**: atualiza valores, gráficos e status automaticamente.

---

## 7. Arquitetura IoT na Simulação

O sistema se enquadra nas camadas clássicas da IoT da seguinte forma:

| Camada                                      | Função na Simulação                                                                                                 |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Camada de Percepção (Perception Layer)**  | Sensores de temperatura e humidade (simulados via `sensor.py`). Captura os dados do ambiente.                       |
| **Camada de Rede (Network Layer)**          | Comunicação HTTP entre o sensor e o servidor. Transmite dados via rede local (hotspot).                             |
| **Camada de Aplicação (Application Layer)** | Dashboard web em `index.html`, gráficos Chart.js, lógica de decisão para irrigação.                                 |
| **Dispositivos Edge**                       | Celular rodando o servidor (`server.py`). Processa dados recebidos, decide rega automática e entrega interface web. |

---

## 8. Componentes IoT na Simulação

| Tipo                              | Dispositivo/Simulado                                                                 | Função                                                                           |
| --------------------------------- | ------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------- |
| **Sensores**                      | Sensor de temperatura e humidade (`sensor.py`)                                       | Captura dados ambientais em tempo real.                                          |
| **Atuadores**                     | Regador simulado (efeito no sensor: diminuição de temperatura e aumento de humidade) | Simula ação de regar a plantação.                                                |
| **Dispositivos Edge**             | Servidor Flask no celular 1                                                          | Recebe dados dos sensores, processa lógica de irrigação e fornece dashboard web. |
| **Dispositivos de Monitoramento** | PC ou outro navegador                                                                | Visualiza o dashboard, gráficos e status em tempo real.                          |

---

## 9. Como Rodar

### Passo 1 – Servidor (Celular 1)

```bash
pip install -r requirements.txt
python server.py
```

* Liga hotspot para rede local.

### Passo 2 – Sensor (Celular 2)

```bash
pip install requests
python sensor.py
```

### Passo 3 – Dashboard (PC ou outro dispositivo)

* Abrir navegador:

```
http://IP_DO_SERVIDOR:5000
```

### Passo 4 – Webcam

* Instalar **IP Webcam** no celular do servidor.
* Copiar link `http://IP_DO_SERVIDOR:8080/video` para a tag `<img>` do dashboard (já configurado).

---

## 10. Observações

* Lógica de rega automática evita excesso de irrigação.
* Simulação permite testar interações manual e automática.
* Pode ser expandido com alertas, histórico em SQLite ou integração com dispositivos reais.

---

** Conclusão:**
Este projeto demonstra um **sistema IoT completo** em microescala, integrando sensores, atuadores, dispositivos edge e dashboard web, com **decisão automática baseada em dados** de forma lógica e realista.

