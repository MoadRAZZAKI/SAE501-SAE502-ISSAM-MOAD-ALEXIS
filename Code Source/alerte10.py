import tkinter as tk
from tkinter import ttk
import customtkinter
#import netifaces
import subprocess
from tkinter import filedialog
import time
import csv
import psutil
from sniff10 import *
from sniff10 import lancement_sniffing
from sniff10 import traitement_paquet
import time
from tkinter import messagebox
import motor.motor_asyncio
from pymongo import MongoClient, change_stream
import asyncio
import json


customtkinter.set_default_color_theme("green")
customtkinter.set_appearance_mode("dark") 
interfacelist = [interface for interface in psutil.net_if_addrs().keys()]#netifaces.interfaces()
# Récupération des interfaces
#interfacelist = [interface for interface in psutil.net_if_addrs().keys()]#netifaces.interfaces()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.sniffer = None
        self.compteur = 0 #TEST
        self.taille = 0
        self.selected_value = None

        # configure window
        self.title("SNIFFER")
        self.geometry(f"{2000}x{2000}")

        # configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((0,1,2), weight=2)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=100,height=100, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Sniffer", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame,command=self.save_selected_items_to_file, text="Save")#command=self.sauvegarder_contenu_arborescence
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event_start, text='Start')
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event_stop, text='Stop')
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, command=self.button_fonction, text='Import')
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, command=self.refresh, text='refresh')
        self.sidebar_button_4.grid(row=5, column=0, padx=20, pady=10)
        

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Thèmes:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Zoom:", anchor="w")
        self.scaling_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20))

        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=180)
        self.tabview.grid(row=0, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.tabview.add("Interfaces")
        self.tabview.tab("Interfaces").grid_columnconfigure(0, weight=3)  # configure grid of individual tabs
        self.selected_interface = customtkinter.StringVar()
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Interfaces"), dynamic_resizing=True,
                                                        values=interfacelist, variable=self.selected_interface)
        
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.buttonnewpage = customtkinter.CTkButton(self,text="Alerte",command=lambda path="graph2.py": self.execute_script(path))
        self.buttonnewpage.grid(row=1,column=2,sticky="n",pady=(40,0))
        #interfacelist, variable=self.selected_interface
        self.selected_interface.trace_add('write', self.interface_changed)

        
        #self.my_entry = customtkinter.CTkEntry(self, font=("Helvetica", 20),width=1000,textvariable=self.my_entry)
        #self.my_entry.grid(column=1,row=0,sticky="nw",pady=(10, 0),padx=(20,0))
        
        self.search_entry_var = customtkinter.StringVar()
        self.search_entry = customtkinter.CTkEntry(self, textvariable=self.search_entry_var,font=("Helvetica", 20))
        self.search_entry.grid(row=0, column=1, padx=(0, 0), pady=(10, 0), sticky="nwe")
        self.search_entry.bind("<Return>", self.search)
        
        self.search_entry1 = customtkinter.CTkEntry(self, width=170, font=("Helvetica", 15))
        self.search_entry1.grid(row=1, column=2, padx=(30, 0), pady=(110, 0), sticky="nw")
        self.search_entry1.bind("<Return>", self.search1)
        
        self.alerte_label1 = customtkinter.CTkLabel(self, text="Mac DHCP", font=customtkinter.CTkFont(size=15))
        self.alerte_label1.grid(row=1, column=2, padx=(30,0), pady=(80, 0), sticky="nw")
        
        self.packet_tree_frame = customtkinter.CTkFrame(self)
        self.packet_tree_frame.grid(row=0, column=1,rowspan=2, padx=(30, 0), pady=(50, 0), sticky="nsw")
        self.packet_tree_frame.grid_rowconfigure(0, weight=1)
        self.packet_tree_frame.grid_columnconfigure(0, weight=1)

        self.packet_tree = ttk.Treeview(self.packet_tree_frame, columns=('Numero', 'Time', 'IP SRC', 'IP DST','Type','macsrc','macdst','INFO'))
        self.packet_tree.heading('Numero', text='Numero')
        self.packet_tree.column('#1', width=75)
        self.packet_tree.heading('Time', text='Time')
        self.packet_tree.column('#2', width=90)
        self.packet_tree.heading('IP SRC', text='IP SRC')
        self.packet_tree.column('#3', width=200)
        self.packet_tree.heading('IP DST', text='IP DST')
        self.packet_tree.column('#4', width=200)
        self.packet_tree.heading('Type', text='Type')
        self.packet_tree.column('#5', width=200)
        self.packet_tree.heading('macsrc', text='macsrc')
        self.packet_tree.column('#6', width=200)
        self.packet_tree.heading('macdst', text='macdst')
        self.packet_tree.column('#7', width=200)
        self.packet_tree.heading('INFO', text='INFO')
     

        self.numero_ligne = 1

        # Ajouter des éléments à l'arborescence 
        #self.ajouter_element_arborescence("192.168.1.1", "192.168.1.2","DHCPACK","10.10.10.10","macdst","Informations 1","time")
        #self.ajouter_element_arborescence("192.168.1.6", "192.168.1.2","DHCPACK","10.10.10.10","macdst","Informations 1","time")
        
        #self.ajouter_element_arborescence("192.168.1.5", "192.168.1.2","DHCPACK","11.10.10.10","macdst","Informations 1","time")
        #self.ajouter_element_arborescence("192.168.1.2", "192.168.1.2","DHCPDECLINE","10.10.10.10","macdst","Informations 1","time")
        #self.ajouter_element_arborescence("192.168.1.3", "192.168.1.2","DHCPREQUEST","11.10.10.10","macdst","Informations 1","time")
        #self.ajouter_element_arborescence("192.168.1.4", "192.168.1.2","DHCPDECLINE","11.10.10.10","macdst","Informations 1","time")
        #self.ajouter_element_arborescence("192.168.1.1", "192.168.1.2","DHCPNAK","10.10.10.10","macdst","Informations 1","time")
        #self.ajouter_element_arborescence("192.168.1.1", "192.168.1.2","DHCPOFFER","10.10.10.10","macdst","Informations 1","time")
        #self.ajouter_element_arborescence("192.168.1.1", "192.168.1.2","DHCPOFFER","11.10.10.10","macdst","Informations 1","time")
        self.packet_tree.bind("<Double-1>", self.item_double_clicked)
        self.packet_tree.column("#0", width=0, stretch=tk.NO)
        self.packet_tree.pack(fill="both", expand=True)
        # Partie test : 
        # Associer la fonction item_double_clicked au double clic sur un élément


       #Test 1 : SPAM (dans le cas ou  1 même mac demande plusieur adresse ip)
        self.spam()
        #self.ajouter_element_arborescence("192.168.1.1", "192.168.1.2","DHCPREQUEST","10.10.10.10","macdst","Informations 1","time")
        #self.ajouter_element_arborescence("192.168.1.6", "192.168.1.2","DHCPREQUEST","10.10.10.10","macdst","Informations 1","time")
        
        self.ajouter_element_arborescence("192.168.1.5", "192.168.1.2","DHCPACK","d0:7e:28:d2:84:8c","macdst","info 3","time")
        self.ajouter_element_arborescence("192.168.1.5", "192.168.1.2","DHCPACK","10.10.10.10","macdst","Informations 1","time")
        self.ajouter_element_arborescence("192.168.1.2", "192.168.1.2","DHCPDECLINE","10.10.10.10","macdst","Informations 1","time")
        self.ajouter_element_arborescence("192.168.1.2", "192.168.1.2","DHCPDECLINE","d0:7e:28:d2:84:8c","macdst","Informations 1","time")
        self.ajouter_element_arborescence("192.168.1.3", "192.168.1.2","DHCPREQUEST","11.10.10.10","macdst","Informations 1","time")
        self.ajouter_element_arborescence("192.168.1.4", "192.168.1.2","DHCPREQUEST","d0:7e:28:d2:84:8c","macdst","Informations 1","time")
        self.ajouter_element_arborescence("192.168.1.3", "192.168.1.2","DHCPREQUEST","10.10.11.10","macdst","Informations 1","time")
        self.ajouter_element_arborescence("192.168.1.4", "192.168.1.2","DHCPREQUEST","d0:7e:28:d2:84:8c","macdst","Informations 1","time")
        # Test2 : 
        #self.timestamps = []
        # la fonction rajoute plein de paquet (si il y en a plus de 25 en 10 seconde alors un message apparait)
        #self.ajouter_element_periodiquement()
        #d0:7e:28:d2:84:8c
        # Test3 :si je spécifie dans la bare de recherche de droite une adresse mac, alors touts les paquets de types  : Offer ,decline, ack  NAK qui ne possède pas la même adresses provoquerons une alerte
        #self.ajouter_element_arborescence("192.168.1.5", "192.168.1.2","DHCPACK","10.10.10.10","macdst","Informations 1","time")
        #self.ajouter_element_arborescence("192.168.1.5", "192.168.1.2","DHCPACK","11.10.10.10","macdst","Informations 1","time")
        #self.ajouter_element_arborescence("192.168.1.2", "192.168.1.2","DHCPNACK","10.10.10.10","macdst","Informations 1","time")
        #self.ajouter_element_arborescence("192.168.1.2", "192.168.1.2","DHCPNACK","11.10.10.10","macdst","Informations 1","time")
        #self.ajouter_element_arborescence("192.168.1.3", "192.168.1.2","DHCPDECLINE","10.10.10.10","macdst","Informations 1","time")
        #self.ajouter_element_arborescence("192.168.1.4", "192.168.1.2","DHCPDECLINE","11.10.10.10","macdst","Informations 1","time")
        #self.ajouter_element_arborescence("192.168.1.3", "192.168.1.2","DHCPOFFER","10.10.10.10","macdst","Informations 1","time")
        #self.ajouter_element_arborescence("192.168.1.4", "192.168.1.2","DHCPOFFER","11.10.10.10","macdst","Informations 1","time")
        #self.ajouter_element_arborescence("192.168.1.3", "192.168.1.2","DHCPRELEASE","10.10.10.10","macdst","Informations 1","time")
        #self.ajouter_element_arborescence("192.168.1.4", "192.168.1.2","DHCPRELEASE","10.10.10.10","macdst","Informations 1","time")
        
        
        

    # Changement de l'apparance
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)


    # Changement du scaling
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    # Action sur la side bar
    def sidebar_button_event_start(self):
        print("Lancement du sniffer")
        #lancement_sniffing("enp0s31f6")
        self.sniffer = lancement_sniffing(self.selected_value)
        self.sniffer.start()
    
    def refresh(self):
        if self.taille != len(liste_paquets):
            for paquet in liste_paquets[self.compteur:len(liste_paquets)]:
                current_time, ip_src, ip_dst, type_paquet, mac_src, mac_dst, paquet = transfert_interface(paquet)
                self.ajouter_element_arborescence(ip_src, ip_dst, type_paquet, mac_src,mac_dst,paquet,current_time)
                self.compteur = len(liste_paquets)
            self.taille = len(liste_paquets)
    
    def affichage(self,paquet):
        current_time, ip_src, ip_dst, type_paquet, mac_src, mac_dst, paquet = transfert_interface(paquet)
        self.ajouter_element_arborescence(ip_src, ip_dst, type_paquet, mac_src,mac_dst,paquet,current_time)
    
    def sidebar_button_event_stop(self):
        print("Arrêt du sniffer")
        self.sniffer.stop()


    def execute_script(self,script_path):
        try:
            subprocess.run(['python3', script_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Une erreur s'est produite lors de l'exécution du script : {e}")

    def ajouter_element_arborescence(self, ip_src, ip_dst, request, macsrc,macdst,info, current_time):
        #current_time = time.strftime("%H:%M:%S")

        self.packet_tree.insert('', tk.END, values=(self.numero_ligne, current_time, ip_src, ip_dst, request,macsrc,macdst, info))
        # Incrémenter le numéro de ligne
        self.numero_ligne += 1
    
    
    def ajouter_element_periodiquement(self):
        timetest=time.strftime("%H:%M:%S")
        self.ajouter_element_arborescence("192.168.1.1", "192.168.1.2","ACK","10.10.10.10","macdst","Informations 1",timetest)

        # Ajouter l'horodatage actuel à la liste
        self.timestamps.append(datetime.now())

        # Supprimer les horodatages expirés (plus vieux que 10 secondes)
        self.timestamps = [ts for ts in self.timestamps if datetime.now() - ts <= timedelta(seconds=10)]

        # Vérifier si plus de 25 lignes ont été ajoutées dans les 10 dernières secondes
        if len(self.timestamps) > 25:
            messagebox.showwarning("Alerte ", "Plus de 25 paquets en 10 secondes !")
            pass

        delai = random.randint(1, 1) * 100  # Convertir en millisecondes
        self.after(delai, self.ajouter_element_periodiquement)


    def interface_changed(self, *args):
        # Cette fonction sera appelée à chaque fois que la valeur de la variable change
            self.selected_value = self.selected_interface.get()
            print("Vous avez sélectionné l'interface", self.selected_value)
    

    #def item_double_clicked(self, event):
       # Fonction appelée lorsqu'un élément de l'arborescence est double-cliqué
    #    item = self.packet_tree.selection()[0]
    #    values = self.packet_tree.item(item, 'values')
    #    print("Double clic sur l'élément:", values)
 
    def item_double_clicked(self, event):
        # Fonction appelée lorsqu'un élément de l'arborescence est double-cliqué
        item = self.packet_tree.selection()[0]
        values = self.packet_tree.item(item, 'values')
    
    # Créer une nouvelle fenêtre
        new_window = tk.Toplevel(self)
        new_window.geometry("800x500")
        new_window.title("Paquet Sélectionné")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((0,1,2), weight=2)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        # Définir la valeur à formater
        valeur = values[7]

        # Formater la valeur sur 90 caractères avec un retour à la ligne
        valeur_formatee = '\n'.join([valeur[i:i+120] for i in range(0, len(valeur), 120)])

        # Créer le texte avec la valeur formatée
        textcustom = (
            " Paquet numéro :" + values[0] + "\n\n" +
            "Heure : " + values[1] + "\n\n" +
            "Ip source :" + values[2] + "\n\n" +
            "Ip destination : " + values[3] + "\n\n" +
            "Type :" + values[4] + "\n\n" +
            "MAC source : " + values[5] + "\n\n" +
            "MAC destination : " + values[6] + "\n\n" +
            "Info : " + valeur_formatee + "\n\n"
        )

        # Créer le label avec le texte et l'aligner à droite
        label = customtkinter.CTkLabel(new_window, text=f"{textcustom}", text_color="black", justify='left')

        # Afficher le label dans la fenêtre
        label.grid(column=0, row=1, sticky='e')

        

    def save_selected_items_to_file(self):
        
        # Sélectionne tous les éléments de l'arborescence
        items = self.packet_tree.get_children()
        for item in items:
            self.packet_tree.selection_add(item)

        # Récupère les éléments sélectionnés
        selected_items = self.packet_tree.selection()

        # Ouvre la boîte de dialogue pour choisir le fichier
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

        # Vérifie si l'utilisateur a annulé la boîte de dialogue
        if not file_path:
            return

        # Écrit les éléments sélectionnés dans le fichier
        with open(file_path, 'w') as file:
            for item in selected_items:
                values = self.packet_tree.item(item, 'values')
                line = ', '.join(map(str, values))
                file.write(f"{line}\n")


    def afficher_contenu(self, nom_fichier):
       
            try:
                with open(nom_fichier, 'r', encoding='utf-8') as file:
                    contenu = file.read()
                    self.modifier_et_afficher(contenu)
                    print(contenu)
            except FileNotFoundError:
                print("Fichier non trouvé.")
            except Exception as e:
                print(f"Une erreur s'est produite : {str(e)}")

    def modifier_et_afficher(self, data):
        # Diviser les lignes
        lines = data.split('\n')

        for line in lines:
            parts = line.split(', ', 1)
            if len(parts) > 1:
                values = parts[1].split(', ')
                print(values)
                self.import_element_arborescence(*values)

        # Mettre à jour self.numero_ligne à la fin de la boucle
        self.numero_ligne += len(lines)




    def clear_treeview(self):
        self.packet_tree.delete(*self.packet_tree.get_children())

    def button_fonction(self):
        fichier = filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")])
        if fichier:
            self.clear_treeview()
            with open(fichier, 'r', encoding='utf-8') as file:
                contenu = file.read()
            self.modifier_et_afficher(contenu)
    
    def search(self, event):
        search_text = self.search_entry_var.get().lower()
        self.packet_tree.selection_remove(*self.packet_tree.selection())
        for item in self.packet_tree.get_children():
            values = self.packet_tree.item(item)['values']
            if any(isinstance(value, str) and search_text in value.lower() for value in values):
                self.packet_tree.selection_add(item)
                self.packet_tree.move(item, '', '0')
                self.packet_tree.see(item)
    
    def alertespam(self):
        for item in self.packet_tree.get_children():
            coloneipsrc = self.packet_tree.item(item, 'values')[1]
            print(coloneipsrc)
            
    def search1(self, event):
    # Récupérer la valeur de l'Entry
        search_text = self.search_entry1.get()
        self.alerte_label1.configure(text=search_text)
        compteur = 0
        liste_id = []
        
        # Parcourir les éléments du Treeview
        for item in self.packet_tree.get_children():
            # Récupérer la valeur de la colonne 'Type' pour cet élément
            packet_type = self.packet_tree.item(item, 'values')[4]  # La colonne 'Type' est indexée à 4

            # Vérifier si le type est 'Offer', 'Decline', 'Ack' ou 'NAK'
            if packet_type in ['DHCPOFFER', 'DHCPDECLINE', 'DHCPACK', 'DHCPNACK']:
                # Récupérer la valeur de la colonne 'macsrc' pour cet élément
                macsrc_value = self.packet_tree.item(item, 'values')[5]  # La colonne 'macsrc' est indexée à 5

                # Vérifier si la valeur de 'macsrc' correspond à la recherche
                if search_text == macsrc_value:
                    # Sélectionner cet élément dans le Treeview
                    pass  # Sortir de la boucle dès que la valeur est trouvée
                else:
                    compteur += 1
                    id = self.packet_tree.item(item, 'values')[0]
                    liste_id.append(id)
                               
            else:
                # Si la boucle s'exécute sans interruption (c'est-à-dire que la valeur n'a pas été trouvée)
                print("Aucun paquet de type Offer, Decline, Ack ou NAK avec la valeur macsrc correspondante n'a été trouvé.")
        
        if compteur > 0:
            messagebox.showinfo( "Alerte !", "Suspicion d'une usurpation de l'adresse MAC du DHCP sur les paquets "+str(liste_id))


    def spam(self):
        duplicates = {}  # Dictionnaire pour stocker les paires d'adresses MAC et IP

        # Parcourir tous les éléments du Treeview
        for item in self.packet_tree.get_children():
            # Récupérer le type du paquet
            packet_type = self.packet_tree.item(item, 'values')[4]

            # Vérifier si le type du paquet est "DHCPREQUEST"
            if packet_type == "DHCPREQUEST":
                # Récupérer l'adresse MAC et l'adresse IP de l'élément actuel
                macsrc = self.packet_tree.item(item, 'values')[5]
                ipsrc = self.packet_tree.item(item, 'values')[6]

                # Vérifier si cette paire MAC-IP existe déjà dans le dictionnaire
                if (macsrc, ipsrc) in duplicates:
                    # Si c'est le cas, ajouter l'ID de l'élément actuel à la liste des doublons
                    duplicates[(macsrc, ipsrc)].append(self.packet_tree.item(item, 'values')[0])
                else:
                    # Sinon, ajouter cette paire au dictionnaire avec l'ID de l'élément actuel comme valeur
                    duplicates[(macsrc, ipsrc)] = [self.packet_tree.item(item, 'values')[0]]

        # Filtrer les doublons
        duplicates = {key: value for key, value in duplicates.items() if len(value) > 1}

        # Afficher les doublons s'il y en a
        if duplicates:
            message = "\n"
            for (mac, ip), packets in duplicates.items():
                message += f"Les paquets : {', '.join(map(str, packets))}\n"+"demande une adresse ip avec la même adresse mac"+"\n"
            messagebox.showinfo("Attention SPAM", message)

    def import_element_arborescence(self,time, ip_src,ip_dst, request,macsrc,macdst, info):
            
            self.packet_tree.insert('', tk.END, values=(self.numero_ligne, time, ip_src, ip_dst, request,macsrc,macdst, info))
            # Incrémenter le numéro de ligne
            self.numero_ligne += 1

#if __name__ == "__main__":
app = App()
app.mainloop()

async def watch_collection():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://root:password@10.203.0.149:27017")
    db = client['data']
    collection = db["packet_dhcp"]
    change_stream = collection.watch()
    while True:
        change = await change_stream.next()
        paquet = json.loads(change)



# Offer ,decline, ack  NAK