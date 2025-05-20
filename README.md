# Digital Twin for DDC Systems

This project simulates a containerized **Digital Twin** for a **Direct Digital Control (DDC)** system using real-time telemetry, MQTT messaging, and an interactive web dashboard.  
Designed for secure, offline deployment, the system is built entirely with Docker Compose and supports integration with legacy protocols such as DNP3.

---

##  Institutional Affiliation

Developed in collaboration with:

- **NAVFAC EXWC – U.S. Navy**

---

##  Research Goals

This project explores:

- Containerized simulation of control systems
- Real-time telemetry publishing using MQTT and Python
- Interactive dashboards via Flask and Socket.IO
- Legacy protocol integration (e.g., DNP3)
- Secure, air-gapped deployment with open-source tooling

---

## 🔧 Features

- Real-time temperature simulation via `sensor.py`
- MQTT broker (Eclipse Mosquitto) for pub/sub messaging
- Virtual PLC that processes sensor data
- Flask-based dashboard with live updates (Socket.IO)
- Optional DNP3 outstation container (OpenDNP3)
- Fully containerized with Docker Compose
- Designed for **air-gapped** environments

---
## 📂 Project Structure

```text
sf_digital-twin-ddc/
├── docker/
│   ├── sensors/         # Async temperature publisher (gmqtt)
│   ├── plc/             # Virtual controller logic
│   ├── dashboard/       # Flask + Socket.IO web app
│   ├── dnp3/            # C++ DNP3 outstation build
│   └── broker/          # Mosquitto MQTT config
├── docker-compose.yml   # Container definitions
└── README.md            # This file
```

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Git (optional)

---

### Run the Digital Twin

```bash
git clone https://github.com/gtech29/digital-twin-ddc.git
cd digital-twin-ddc

# Build and start all services
docker-compose up -d --build

#Visit the dashboard:
http://localhost:5000

View real-time logs:
docker-compose logs -f sensor
docker-compose logs -f dashboard
```

### Services Overview

| Service         | Description                            | Port   |
|-----------------|----------------------------------------|--------|
| mqtt-broker     | Mosquitto MQTT server                  | 1883   |
| sensor          | Publishes simulated temperature data   | —      |
| plc             | Subscribes and reacts to sensor data   | —      |
| dashboard       | Flask + Socket.IO dashboard            | 5000   |
| dnp3-outstation | Simulated field device (optional)      | 20000  |
---

## Configuration

**Sensor Publish Rate**  
Modify this line in `docker/sensors/sensor.py` to adjust the frequency of temperature updates:

```python
await asyncio.sleep(2)  # Publishes every 2 seconds
[ Sensor ] ---> MQTT ---> [          PLC            ]
                                ↘           ↘
                         [ Dashboard ]   [ DNP3 Outstation ]
```

## Licensing and Use

This repository is public for educational and research purposes.  
Unless otherwise noted, it is released under the **MIT License**.

For military, commercial, or mission-critical use, conduct proper security validation and licensing review.

---

## Author

**Juan Rodriguez**  
Digital Twin Developer  
CSUN Computer Science | NAVFAC EXWC Intern  
GitHub: [@gtech29](https://github.com/gtech29)

---

## Contact

For questions, collaboration, or demo requests:  
Open an issue or reach out via GitHub.

---

```bash
# After pasting into your README.md, commit it:
git add README.md
git commit -m "Add complete README with project overview and research context"
git push
```

MIT License

Copyright (c) 2025 Juan Rodriguez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
---

## Contributors

Thanks to the following individuals for their support and collaboration:

- **Juan Rodriguez** – Developer, Maintainer  
  [@gtech29](https://github.com/gtech29)

Contributions are welcome!  
Feel free to submit a pull request or open an issue.
---

![Docker](https://img.shields.io/badge/Containerized-Docker-blue?logo=docker)
![MQTT](https://img.shields.io/badge/Messaging-MQTT-orange?logo=mqtt)
![Flask](https://img.shields.io/badge/WebApp-Flask-black?logo=flask)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Made with Python](https://img.shields.io/badge/Python-3.11-blue.svg?logo=python)

