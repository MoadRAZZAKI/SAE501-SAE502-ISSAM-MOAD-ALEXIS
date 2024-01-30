from scapy.all import *
import netifaces
import json


#interfaces = netifaces.interfaces()  #Liste des interfaces réseau de la machine

class Paquet:
    def __init__(self, paquet) -> None:
        #self.affiche = paquet.show()
        #self.contenu = 
        def affiche_paquet(self):
            #print(self.affiche)
            return None

        
            

class Liste_paquets:
    def __init__(self) -> None:
        self.liste = []
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

        self.dictionnaire = {
            "Type": None,
            "Ether":
                {
                    "dst": None,
                    "src": None,
                    "type": None
                },
            "IP":
                {
                    "version": None,
                    "src": None,
                    "dst": None,
                    "ttl": None
                },
            "DHCP":
                {
                    #"requested_addr": None,
                    #"hostname": None
                    "options":
                    {
                        "hostname": None,
                        "requested_addr": None,
                        "message-type": None
                    }
                    
                },
            "UDP":
                {
                    "sport": None,
                    "dport": None,
                    "len": None
                },
            "BOOTP":
                {   
                    "ciaddr": None,
                    "yiaddr": None,
                    "siaddr": None,
                    "giaddr": None,
                    "chaddr": None
                }   
         }
    
    def ajoute(self, element):
        self.liste.append(element)

paquets = Liste_paquets()