import tkinter as tk
from tkinter import ttk
import customtkinter
#import netifaces
import subprocess
from tkinter import filedialog
import time
import csv
import psutil

customtkinter.set_default_color_theme("green")
interfacelist = [interface for interface in psutil.net_if_addrs().keys()]#netifaces.interfaces()
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

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
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event, text='Start')
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event, text='Stop')
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, command=self.button_fonction, text='Import')
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)
        

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
        
        self.buttonnewpage = customtkinter.CTkButton(self,text="API")
        self.buttonnewpage.grid(row=1,column=2,sticky="s")
        #interfacelist, variable=self.selected_interface
        self.selected_interface.trace_add('write', self.interface_changed)

        self.search_entry_var = customtkinter.StringVar()
        self.search_entry = customtkinter.CTkEntry(self, textvariable=self.search_entry_var,width=1310,font=("Helvetica", 20))
        self.search_entry.grid(row=0, column=1, padx=(20, 0), pady=(10, 0), sticky="nw")
        self.search_entry.bind("<Return>", self.search)  
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
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
        self.packet_tree.column('#3', width=120)
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
        self.ajouter_element_arborescence("192.168.1.1", "192.168.1.2","Request","00:1B:44:11:3A:B7","00:1B:44:11:3A:B7","Informations 1")
        self.ajouter_element_arborescence("192.168.1.3", "192.168.1.4","discover","00:1B:44:11:3A:B7","00:1B:44:11:3A:B7", "Informations 2")
        self.ajouter_element_arborescence("192.168.1.3", "192.168.1.4","offer","00:1B:44:11:3A:B7","00:1B:44:11:3A:B7", "Informations 2")
        self.ajouter_element_arborescence("192.168.1.3", "192.168.1.4","offer", "00:1B:44:11:3A:B7","macdst","Informations 2fhizuebfiube")
        self.packet_tree.bind("<Double-1>", self.item_double_clicked)
        self.packet_tree.column("#0", width=0, stretch=tk.NO)
        self.packet_tree.pack(fill="both", expand=True)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    # Changement du scaling
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    # Action sur la side bar
    def sidebar_button_event(self):
        print("sidebar_button click")

    def ajouter_element_arborescence(self, ip_src, ip_dst, request, macsrc,macdst,info):
        current_time = time.strftime("%H:%M:%S")
        self.packet_tree.insert('', tk.END, values=(self.numero_ligne, current_time, ip_src, ip_dst, request,macsrc,macdst, info))
        # Incrémenter le numéro de ligne
        self.numero_ligne += 1
    

    def import_element_arborescence(self,time, ip_src, ip_dst, request,macsrc,macdst,info):
        
        self.packet_tree.insert('', tk.END, values=(self.numero_ligne, time, ip_src, ip_dst, request, macsrc,macdst, info))
        # Incrémenter le numéro de ligne
        self.numero_ligne += 1

    def interface_changed(self, *args):
        # Cette fonction sera appelée à chaque fois que la valeur de la variable change
            selected_value = self.selected_interface.get()
            print("Vous avez sélectionné l'interface", selected_value)

    def item_double_clicked(self, event):
        # Fonction appelée lorsqu'un élément de l'arborescence est double-cliqué
        item = self.packet_tree.selection()[0]
        values = self.packet_tree.item(item, 'values')
    
    # Créer une nouvelle fenêtre
        new_window = tk.Toplevel(self)
        new_window.geometry("800x500")
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((0,1,2), weight=2)
        self.grid_rowconfigure((0, 1, 2), weight=1)

    # Afficher la valeur de 'values' dans la nouvelle fenêtre
        textcustom=" Paquet numéro :"+values[0]+"\n\n"+"Heure : "+values[1]+"\n\n"+"Ip destination :"+values[2]+"\n\n"+"Ip source : "+values[3]+"\n\n"+"Type :"+values[4]+"\n\n"+"Info : "+values[5]+"\n\n"
        label = customtkinter.CTkLabel(new_window, text=f"{textcustom}",text_color="black")
        
        label.grid(column=0,row=1)
        

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

 
if __name__ == "__main__":
    app = App()
    app.mainloop()