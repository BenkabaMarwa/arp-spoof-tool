# 🔥 ARP Spoofing Tool (Educational Purpose Only)

This project is a simple **ARP spoofing / ARP poisoning tool** written in Python using **Scapy**.  
It demonstrates how attackers can manipulate the ARP table of a victim and gateway to perform **Man-in-the-Middle (MITM)** attacks.

⚠️ **Disclaimer:**  
This tool is created for **educational and research purposes only**.  
Do **NOT** use it on networks without proper authorization. Unauthorized use is **illegal**.

---

## 📌 Features
- Retrieve MAC addresses of target and gateway automatically.  
- Send **fake ARP replies** to poison the ARP table of victim and gateway.  
- Restore original ARP tables on exit (Ctrl+C).  
- Supports specifying victim MAC manually.  

---

## ⚙️ Requirements
- Python **3.x**
- [Scapy](https://scapy.readthedocs.io/)

Install Scapy with:
```bash
pip install scapy
