from scapy.all import *
#from alerte3 import *
import json

import pymongo #TEST
import motor.motor_asyncio
from pymongo import MongoClient, change_stream
import asyncio

client = pymongo.MongoClient("192.168.39.209", username="root", password="password")
database = client["data"]
collection = database["packet_dhcp"]

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

def transfert_interface(paquet):
    ip_src,ip_dst = paquet['IP']['src'], paquet['IP']['dst']
    type_paquet = paquet['Type']
    mac_src,mac_dst = paquet['Ethernet']['src'], paquet['Ethernet']['dst']
    info = paquet
    current_time = paquet['time']
    return current_time, ip_src, ip_dst, type_paquet, mac_src, mac_dst, paquet


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

'''def convertir_en_types_json_serializables(dico):
    dico_serializable = {}
    for cle, valeur in dico.items():
        if isinstance(valeur, FlagValue):
            valeur = str(valeur)  # Convertir le FlagValue en chaîne de caractères
        dico_serializable[cle] = valeur
    return dico_serializable'''

def flag_to_str(dico):
    dico["IP"]["flags"] = str(dico["IP"]["flags"])
    dico["BOOTP"]["flags"] = str(dico["BOOTP"]["flags"])


def convertir_en_types_json_serializables(dico):
    for cle, valeur in dico.items():
        if isinstance(valeur,dict):
            for k,v in valeur.items():
                if isinstance(v, FlagValue):
                      # Convertir le FlagValue en chaîne de caractères
                    dico[cle][k] = str(v)
                if isinstance(v, bytes):
                    dico[cle][k] = dico[cle][k].decode(errors='ignore')
    return dico


def affichage_auto(paquet):
    dico = dict()
    dico["time"] = time.strftime("%H:%M:%S")
    type_msg = type_message[paquet[DHCP].getfieldval('options')[0][1]]
    dico['Type'] = type_msg
    layers = get_packet_layers(paquet)
    for layer in layers:
        dico[layer] = {}
        for field in paquet[layer].fields_desc:
            dico[layer][field.name] = None
            if field.name == 'options' and layer == "DHCP options": 
                options = list(paquet[DHCP].options)
                options = [element for element in options if type(element)==tuple]
                dico[layer]= dict(options)
                continue
            try:
                dico[layer][field.name] = paquet[layer].getfieldval(field.name)
            except AttributeError:
                print(f"Erreur sur l'attribut {field.name}")
                pass
    print(dico)
    #traitement_par_type[type_msg](dico)
    global collection
    dico = convertir_en_types_json_serializables(dico)
    #dico_json = json.dumps(convertir_en_types_json_serializables(dico))
    collection.insert_one(dico)
    #collection.insert_one({'Ethernet': {'dst': 'ff:ff:ff:ff:ff:ff', 'src': 'b0:7b:25:26:9a:d9', 'type': 2048}})

def get_packet_layers(packet):
    layer_list = []
    layer = packet
    while layer:
        layer_list.append(layer.name)
        layer = layer.payload
    return layer_list

def traitement_paquet(paquet):
    affichage_auto(paquet)
    #paquet = Paquet(paquet)


    

def lancement_sniffing(interface,*args):
    print("Lancement du sniffer")
    #sniff(filter="udp port 67 or 68", count=6,prn=traitement_paquet,iface=interface)
    sniffer = AsyncSniffer(prn=traitement_paquet,iface=interface, filter="udp port 67 or 68")
    return sniffer

'''async def watch_collection(app):
        # Créer une connexion à MongoDB
        client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://root:password@192.168.39.209:27017')

        # Sélectionner votre base de données et votre collection
        db = client['data']
        collection = db['packet_dhcp']

        # Créer un ChangeStream
        change_stream = collection.watch()
        # Boucle infinie pour écouter les nouvelles modifications
        while True:
            change = await change_stream.next()
            print(change)
            app.affiche_paquet(json.loads(change))
'''

