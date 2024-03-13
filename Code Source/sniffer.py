from scapy.all import *
import json

import pymongo
import motor.motor_asyncio
from pymongo import MongoClient, change_stream
import asyncio

IP_BDD = "192.168.39.209" #Renseignez ici l'adresse ip de votre serveur


#Configuration de l'authentification à la base de données
client = pymongo.MongoClient(IP_BDD, username="root", password="password")
database = client["data"]
collection = database["packet_dhcp"]



type_message = { #Dictionnaire de l'ensemble des types de paquets DHCP possibles
            1: "DHCPDISCOVER",
            2: "DHCPOFFER",
            3: "DHCPREQUEST",
            4: "DHCPDECLINE",
            5: "DHCPACK",
            6: "DHCPNAK",
            7: "DHCPRELEASE",
            8: "DHCPINFORM",
        }


#Traitement des paquets en fonction de leur type pour affichage en console
def discover(paquet):
    print("DHCPDISCOVER")

def offer(paquet):
    print("DHCPOFFER")

def request(paquet):
    print("DHCPREQUEST")

def ack(paquet):
    print("DHCPACK")

def release(paquet):
    print(f"DHCPRELEASE")
    
def decline(paquet):
    print(f"DHCPDECLINE")
    
def nak(paquet):
    print(f"DHCPNAK")
    
def inform(paquet):
    print(f"DHCPINFORM")

traitement_par_type = { # ce dictionnaire permet d'exécuter la fonction adéquate en fonction du type de paquet pour un affichage en console
    "DHCPDISCOVER": discover,
    "DHCPOFFER": offer,
    "DHCPREQUEST": request,
    "DHCPDECLINE": decline,
    "DHCPACK": ack,
    "DHCPNAK": nak,
     "DHCPRELEASE": release,
    "DHCPINFORM": inform
}


def transfert_interface(paquet):
    '''
    Cette fonction permet de séléctionner dans le paquet les informations à afficher dans l'interface graphique
    Cette fonction est appelée par le programme "interface_graphique.py" lors de la réception d'un paquet

