from scapy.all import *
#from alerte3 import *



class Paquet:
    def __init__(self, paquet) -> None:
        self.paquet = paquet
        self.type_message = {
            1: "DHCPDISCOVER",
            2: "DHCPOFFER",
            3: "DHCPREQUEST",
            4: "DHCPDECLINE",
            5: "DHCPACK",
            6: "DHCPNAK",
            7: "DHCPRELEASE",
            8: "DHCPINFORM",
        }


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
    print("DHCPDISCOVER EMIS PAR la machine "+str(paquet['DHCP options']['hostname']))

def offer(paquet):
    print("DHCPOFFER EMIS PAR le serveur "+paquet['DHCP options']['server_id'])

def request(paquet):
    print("DHCPREQUEST || Le client "+str(paquet['DHCP options']['hostname'])+" souhaites obtenir l'IP "+paquet['DHCP options']['requested_addr'])

def ack(paquet):
    print("DHCPACK || Le serveur "+paquet['DHCP options']['server_id']+" attribue l'adresse au client")

def release(paquet):
    print(f"DHCPRELEASE")
    
def decline(paquet):
    print(f"DHCPDECLINE")
    
def nak(paquet):
    print(f"DHCPNAK")
    
def inform(paquet):
    print(f"DHCPINFORM")

