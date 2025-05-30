# Digital Twin for DDC (Direct Digital Control) System

This project simulates a Direct Digital Control (DDC) system using containerized components. It virtualizes physical elements like sensors, a PLC (Programmable Logic Controller), and a real-time dashboard. Designed for experimentation, development, and future deployment using Kubernetes.

---

## Architecture Overview

```
[ Sensor ] ---> [ MQTT Broker ] ---> [ PLC ] ---> [ Dashboard UI ]
     │                                     ↑
     └─────────────────────────────────────┘
```

All components communicate over a custom Docker bridge network (`twin-net`) using MQTT. The setup is fully containerized using Docker and can be orchestrated via Docker Compose or Kubernetes.

---

## Tech Stack

- **Python** — service logic
- **Docker** — containerization
- **MQTT (Mosquitto)** — messaging protocol
- **Flask + Flask-SocketIO** — real-time web dashboard
- **Chart.js** — temperature graphing
- **Kubernetes (K8s)** — for orchestration (included under `/K8s`)

---

## How to Run It Locally

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/digital-twin-ddc.git
cd digital-twin-ddc
```

### 2. Build and Launch Containers

```bash
docker compose up --build
```

This will start:
- A simulated temperature sensor
- An MQTT broker (Mosquitto)
- A PLC that reacts to incoming data
- A dashboard for real-time monitoring

### 3. View the Dashboard

Open your browser to:  
[http://localhost:5000](http://localhost:5000)

### 4. (Optional) Send Test MQTT Message

```bash
docker exec -it mqtt-broker mosquitto_pub -h localhost -t sensors/temperature -m "24.7"
```

---

## 📁 Project Structure

```
digital-twin-ddc/
│
├── docker/
│   ├── broker/            # Mosquitto config
│   ├── dashboard/         # Flask app & UI
│   ├── sensors/           # Sensor container
│   └── plc/               # PLC container
│
├── K8s/                   # Kubernetes manifests
├── scripts/               # Utility scripts
├── logs/                  # Local logs
├── .env                   # Environment variables (excluded from repo)
├── docker-compose.yml     # Compose setup for local dev
└── README.md              # You're reading it
```

---

## 🧪 Features

- 📡 Real-time sensor simulation
- 📊 Dynamic temperature dashboard with Chart.js
- 🔌 MQTT message routing via Mosquitto
- 🧱 Modular Docker container setup
- ☁️ Kubernetes-ready structure for scaling

---

## 🔒 Notes

> Make sure to keep sensitive data (such as `.env` or VM configs) excluded using `.gitignore`.

---

## 📄 License

MIT License — open for educational and development use.

---

## 👤 Author

Juan Rodriguez  
[@getch29](https://github.com/gtech29)
