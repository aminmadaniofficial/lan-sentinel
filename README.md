# LAN Sentinel 📡

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)

**LAN Sentinel** is a lightweight, modern, and highly modular local network security monitor built in Python. It periodically scans your local subnet using ARP packets, matches discovered devices with a whitelist of authorized hardware, resolves device manufacturers (vendors) offline, and alerts you instantly through an interactive, color-coded terminal dashboard if an unrecognized device joins your network.

---

## ✨ Features

- **Robust ARP Scanning:** Utilizes `Scapy` to perform fast, low-level Layer 2 network discovery.
- **Modern Packaging:** Packaged cleanly using PEP 517 standard with `pyproject.toml` for easy CLI deployment.
- **Rich Terminal UI (TUI):** Displays scan results in interactive, beautifully formatted tables and live countdown timers using the `rich` library.
- **Offline Vendor Resolution:** Automatically identifies hardware manufacturers (e.g., Apple, Microsoft, Samsung) using a built-in local OUI database (no internet lookup required).
- **Security Intrusion Alerts:** Visual indicators and high-contrast alert panels flag unauthorized devices instantly.
- **Clean Architecture:** Built from the ground up utilizing **SOLID** design principles, proper type hinting, and strict separation of concerns.

---

## 📂 Project Structure

```text
lan-sentinel/
├── config.json             # Network configurations & whitelist
├── pyproject.toml          # Modern python package build configuration
├── README.md               # Project documentation
├── .gitignore              # Standard git ignore patterns
└── src/
    ├── __init__.py
    ├── models.py           # Dataclasses & structure templates
    ├── scanner.py          # Low-level network scanning engine
    ├── storage.py          # Configuration and whitelist managers
    ├── vendor_resolver.py  # Offline OUI hardware manufacturer mapper
    ├── notifier.py         # Rich Terminal UI & alerting logic
    └── main.py             # Application orchestrator
```

---

## 🚀 Installation & Setup

Follow these steps to run LAN Sentinel on your Ubuntu/WSL environment:

### 1. Clone the Repository
```bash
git clone https://github.com/aminmadaniofficial/lan-sentinel.git
cd lan-sentinel
```

### 2. Set Up a Virtual Environment
It is highly recommended to isolate the project dependencies within a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the CLI Tool
Install the project locally in editable mode (this handles all dependencies automatically using `pyproject.toml`):
```bash
pip install -e .
```

---

## ⚙️ Configuration

Before running the tool, edit `config.json` to define your target network subnet and whitelist known devices (authorized devices won't trigger security alarms):

```json
{
  "target_subnet": "192.168.1.0/24",
  "scan_interval_seconds": 60,
  "known_devices": [
    {
      "mac": "00:15:5d:3a:30:a8",
      "name": "Windows Host Gateway"
    }
  ]
}
```

> **Note on WSL 2 Subnets:** If running in WSL 2, use `ip route show | grep default` to find your virtual interface subnet (e.g., `172.30.64.0/24`) and put it under `target_subnet` for local testing.

---

## 🖥️ Usage

Because ARP packet crafting requires raw socket permissions, the application must be executed with root (`sudo`) privileges. Run the CLI tool directly from your virtual environment:

```bash
sudo ./venv/bin/lansentinel
```

### 🌐 Running in WSL 2 (Host Network Mirrored Mode)
If you want WSL to scan your actual physical router network (`192.168.1.X`) instead of the isolated virtual subnet:
1. Open the `%USERPROFILE%` folder in Windows.
2. Edit or create `.wslconfig` and add:
   ```ini
   [wsl2]
   networkingMode=mirrored
   ```
3. Shut down WSL in Windows PowerShell: `wsl --shutdown` and restart Ubuntu.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.