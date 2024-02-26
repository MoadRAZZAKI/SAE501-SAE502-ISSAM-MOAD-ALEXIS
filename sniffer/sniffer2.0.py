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

traitement_par_type = {
    "DHCPDISCOVER": discover,
    "DHCPOFFER": offer,
    "DHCPREQUEST": request,
    "DHCPDECLINE": decline,
    "DHCPACK": ack,
    "DHCPNAK": nak,
     "DHCPRELEASE": release,
    "DHCPINFORM": inform
}


def affichage_auto(paquet):
    dico = dict()
    #dico["Type"] = None
    type_msg = type_message[paquet[DHCP].getfieldval('options')[0][1]]
    dico['Type'] = type_msg
    layers = get_packet_layers(paquet)
    #print("liste des layers ==> "+ str(layers))
    for layer in layers:
        dico[layer] = {}
        for field in paquet[layer].fields_desc:
            #print(f"Le layer c'est {layer} et le field c'est {field.name}")
            #print(f"Le type du layer c'est {type(layer)} et le field c'est {type(field.name)}")
            dico[layer][field.name] = None
            if field.name == 'options' and layer == "DHCP options": 
                #print("je suis dans les options")
                #dico["DHCP"]["options"] = dict(paquet[DHCP].options)
                options = list(paquet[DHCP].options)
                options = [element for element in options if type(element)==tuple]
                #dico[layer][field.name] = dict(options)
                dico[layer]= dict(options)
                continue
                #print("je passe car c'est les options")
                #for element in paquet[DHCP].options:
                #    if type(element) == Tuple:
                #        dico[layer][field.name][element[0]] = dico[layer][field.name][element[1]]
            try:
                 #print(f"{layer} ==> {field.name} = {paquet[layer].getfieldval(field.name)}")
                dico[layer][field.name] = paquet[layer].getfieldval(field.name)
            except AttributeError:
                print(f"Erreur sur l'attribut {field.name}")
                pass
    #print("le type c'est ",type) 
    #print(dico)
    traitement_par_type[type_msg](dico)

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
    

sniff(filter="udp port 67 or 68", count=6,prn=traitement_paquet,iface='Ethernet0')



