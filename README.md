# ONOS Dynamic Network Rerouting with Mininet

This project demonstrates **dynamic flow rerouting** and **link failure monitoring** using the **ONOS SDN controller** (version 2.1.0) and **Mininet**.  
It includes Python scripts that interact with ONOS’s REST API to monitor flows, detect congestion or link failures, and automatically reroute traffic through alternate network paths.

---

## 🚀 Project Overview

- **Controller:** ONOS 2.1.0 (running in Docker)
- **Network Emulator:** Mininet (from official GitHub repo)
- **APIs Used:** ONOS REST API (`onos/v1/devices`, `onos/v1/links`, `onos/v1/flows`)
- **Scripts:**
  - `onos_stats.py` — Retrieves live ONOS network statistics.
  - `dynamic_reroute.py` — Detects flow congestion and reroutes dynamically.
  - `onos_triangle.py` — Monitors link status and performs failover rerouting.

---

# Environment Setup
---
1. Install Docker

If not already installed:
bash
sudo apt update
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker

2. Run ONOS 2.1.0 in Docker
Pull and start the ONOS container:
sudo docker pull onosproject/onos:2.1.0

sudo docker run -d \
  --name onos \
  -p 6653:6653 \
  -p 8181:8181 \
  -p 8101:8101 \
  onosproject/onos:2.1.0

Check if ONOS is running:
sudo docker ps

Access the ONOS GUI:
http://127.0.0.1:8181/onos/ui

Login: onos
Password :rocks

4. Install Mininet
Clone and install Mininet from GitHub:
git clone https://github.com/mininet/mininet.git
cd mininet
sudo ./util/install.sh -a

Verify:
sudo mn --test pingall

5. Connect Mininet to ONOS
Start Mininet and connect it to ONOS:

sudo mn --controller=remote,ip=127.0.0.1,port=6653 --topo tree,2

use your custom topology file:
sudo python3 onos_triangle.py

6. Output

ONOS WEB GUI SHOWING DEVICES CONNECTED IN MINIET 
<img width="1918" height="1078" alt="15" src="https://github.com/user-attachments/assets/5b1aecb0-e68d-4dc1-b2a7-61fb42156f01" />

OUTPUT SHOWING LINK BREAK BETWEEN TWO DEVICES IN ONOS WEB GUI
<img width="1918" height="1078" alt="link down onos gui" src="https://github.com/user-attachments/assets/1c1ba36d-da67-4e50-80ef-9605774eded8" />
