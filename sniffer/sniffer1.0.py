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

def paquet_to_dict(paquet): #Transforme un paquet en dictionnaire
    dictionnaire = paquets.dictionnaire 
    type_message = paquets.type_message
    for layer in dictionnaire.keys():
        if paquet.haslayer(layer):
            if layer == 'DHCP':
                '''message_type, requested_addr, hostname = paquet[DHCP].getfieldval('options')[:3]
                dictionnaire['DHCP']['options']['hostname'] = hostname[1]
                dictionnaire['DHCP']['options']['requested_addr'] = requested_addr[1]
                dictionnaire['DHCP']['options']['message-type'] = message_type[1]
                dictionnaire['Type'] = type_message[message_type[1]]'''
                dictionnaire['Type'] = type_message[paquet[DHCP].getfieldval('options')[0][1]]
                dictionnaire['DHCP']['options'] = paquet[DHCP].getfieldval('options')[1]
            for element in dictionnaire[layer].keys():
                if dictionnaire[layer][element] == None:
                    dictionnaire[layer][element] = paquet[layer].getfieldval(element)
    return dictionnaire

def affiche_paquet(paquet):
    #paquet.show()
    paquet = paquet_to_dict(paquet)
    print(paquet)
    paquets.ajoute(paquet)
    #paquet.show()
    #if paquet.haslayer(DHCP):
        #print("J'ai un paquet DHCP")
     #   dhcp_layer = paquet.getlayer(DHCP)
        #print(dhcp_layer.options)
    
    #print(paquet) #Affiche le contenu complet du paquet


#"udp port 67 or 68"
sniff(filter="udp port 67 or 68", count=0,prn=affiche_paquet,iface='all')
