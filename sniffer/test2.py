from scapy.all import *
import netifaces
import json

type_message = {
            1: "DHCPDISCOVER",
            2: "DHCPOFFER",
            3: "DHCPREQUEST",
            4: "DHCPDECLINE",
            5: "DHCPACK",
            6: "DHCPNAK",
            7: "DHCPRELEASE",
            8: "DHCPINFORM",
        }




def discover(paquet):
    print(f"DHCPDISCOVER EMIS PAR la machine {paquet[DHCP].getfieldval('options')[2][1]}")

def offer(paquet):
    print(f"DHCPOFFER EMIS PAR le serveur {paquet[IP].getfieldval('src')}")

def request(paquet):
    print(f"DHCPREQUEST || Le client souhaites obtenir l'IP {paquet[DHCP].getfieldval('options')[1][1]}")

def ack(paquet):
    print(f"DHCPACK || Le serveur {paquet[IP].getfieldval('src')} attribue l'adresse {paquet[DHCP].getfieldval('options')[4][1]} au client {paquet[DHCP].getfieldval('options')[2][1]}")
