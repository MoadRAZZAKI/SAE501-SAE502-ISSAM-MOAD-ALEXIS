from scapy.all import *
import psutil

interfaces = [interface for interface in psutil.net_if_addrs().keys()]

choix_interface = dict()

texte_demande = "Quelle interface tu veux choisir ?\n"
for i in range(len(interfaces)):
    choix_interface[i] = interfaces[i]
    texte_demande += f"{i}: {interfaces[i]}\n"
    
demande = input(texte_demande)


try:
    interface = choix_interface[int(demande)]
except Exception as e:
    print("Il y'a eu une erreur: ", e)

    

def traitement_paquet(paquet):
    print(paquet.show())

sniff(filter="", count=0,prn=traitement_paquet,iface=interface)