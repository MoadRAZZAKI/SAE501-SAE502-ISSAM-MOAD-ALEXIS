from scapy.all import *



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
    print(f"DHCPDISCOVER EMIS PAR la machine {paquet[DHCP].getfieldval('options')[2][1]}")

def offer(paquet):
    print(f"DHCPOFFER EMIS PAR le serveur {paquet[IP].getfieldval('src')}")

def request(paquet):
    print(f"DHCPREQUEST || Le client souhaites obtenir l'IP {paquet[DHCP].getfieldval('options')[1][1]}")

def ack(paquet):
    print(f"DHCPACK || Le serveur {paquet[IP].getfieldval('src')} attribue l'adresse {paquet[DHCP].getfieldval('options')[4][1]} au client {paquet[DHCP].getfieldval('options')[2][1]}")

traitement_par_type = {
    "DHCPDISCOVER": discover,
    "DHCPOFFER": offer,
    "DHCPREQUEST": request,
#    "DHCPDECLINE": decline,
    "DHCPACK": ack,
#    "DHCPNAK": nak,
#    "DHCPRELEASE": release,
#    "DHCPINFORM": inform
}


def affichage_auto(paquet):
    dico = dict()
    #dico["Type"] = None
    type = type_message[paquet[DHCP].getfieldval('options')[0][1]]
    dico['Type'] = type
    layers = get_packet_layers(paquet)
    #print("liste des layers ==> "+ str(layers))
    for layer in layers:
        dico[layer] = {}
        for field in paquet[layer].fields_desc:
            #print(f"Le layer c'est {layer} et le field c'est {field.name}")
            #print(f"Le type du layer c'est {type(layer)} et le field c'est {type(field.name)}")
            dico[layer][field.name] = None
            if field.name == 'options' and layer == "DHCP": 
                #print("je passe car c'est les options")
                for element in paquet[DHCP].options:
                    if type(element) == Tuple:
                        dico[layer][field.name][element[0]] = dico[layer][field.name][element[1]]
            try:
                 #print(f"{layer} ==> {field.name} = {paquet[layer].getfieldval(field.name)}")
                dico[layer][field.name] = paquet[layer].getfieldval(field.name)
            except AttributeError:
                print(f"Erreur sur l'attribut {field.name}")
                pass
    #traitement_par_type[type](paquet)
    print(dico)

def get_packet_layers(packet):
    layer_list = []
    layer = packet
    while layer:
        layer_list.append(layer.name)
        layer = layer.payload
    return layer_list

def traitement_paquet(paquet):
    affichage_auto(paquet)
    paquet = Paquet(paquet)
    #paquet.affiche_paquet()
    

sniff(filter="udp port 67 or 68", count=0,prn=traitement_paquet,iface='enp0s31f6')



