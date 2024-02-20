from tkinter import ttk, Tk, Frame, Label, Entry, StringVar, messagebox
from datetime import datetime, timedelta
import random

class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Search in Treeview')
        
        self.packet_tree_frame = Frame(root)
        self.packet_tree_frame.grid(row=0, column=1, rowspan=2, padx=(30, 0), pady=(50, 0), sticky="nsw")
        self.packet_tree_frame.grid_rowconfigure(0, weight=1)
        self.packet_tree_frame.grid_columnconfigure(0, weight=1)

        self.packet_tree = ttk.Treeview(self.packet_tree_frame, columns=('Numero', 'Time', 'IP SRC', 'IP DST','Type', 'INFO'))
        self.packet_tree.heading('Numero', text='Numero')
        self.packet_tree.heading('Time', text='Time')
        self.packet_tree.heading('IP SRC', text='IP SRC')
        self.packet_tree.heading('IP DST', text='IP DST')
        self.packet_tree.heading('Type', text='Type')
        self.packet_tree.heading('INFO', text='INFO')
        
        self.packet_tree.grid(row=0, column=0, sticky="nsew")

        # Initialiser le numéro de ligne à 1
        self.numero_ligne = 1

        self.search_label = Label(root, text="Search:")
        self.search_label.grid(row=0, column=0, padx=(20, 0), pady=(50, 0), sticky="e")
        
        self.search_entry_var = StringVar()
        self.search_entry = Entry(root, textvariable=self.search_entry_var)
        self.search_entry.grid(row=0, column=0, padx=(0, 20), pady=(50, 0), sticky="w")
        self.search_entry.bind("<Return>", self.search)

        # Initialiser une liste pour stocker les horodatages de création des lignes
        self.timestamps = []

        # Démarre la fonction pour ajouter un élément avec un délai aléatoire
        self.ajouter_element_periodiquement()

    def ajouter_element_arborescence(self, ip_src, ip_dst, type_, info):
        heure_actuelle = datetime.now().strftime('%H:%M:%S')  # Obtenir l'heure actuelle au format HH:MM:SS
        self.packet_tree.insert('', 'end', text=str(self.numero_ligne),
                                 values=(str(self.numero_ligne), heure_actuelle, ip_src, ip_dst, type_, info))
        self.numero_ligne += 1

    def ajouter_element_periodiquement(self):
        self.ajouter_element_arborescence("192.168.1.1", "192.168.1.2","Request", "Informations 1")

        # Ajouter l'horodatage actuel à la liste
        self.timestamps.append(datetime.now())

        # Supprimer les horodatages expirés (plus vieux que 10 secondes)
        self.timestamps = [ts for ts in self.timestamps if datetime.now() - ts <= timedelta(seconds=10)]

        # Vérifier si plus de 3 lignes ont été ajoutées dans les 10 dernières secondes
        if len(self.timestamps) > 25:
            messagebox.showwarning("Alerte DDOS", "Tentative de DDOS détectée !")
            self.root.quit()


        # Générer un délai aléatoire entre 3 et 10 secondes
        delai = random.randint(1, 1) * 100  # Convertir en millisecondes
        self.root.after(delai, self.ajouter_element_periodiquement)

    def search(self, event):
        search_text = self.search_entry_var.get().lower()
        self.packet_tree.selection_remove(*self.packet_tree.selection())
        for item in self.packet_tree.get_children():
            values = self.packet_tree.item(item)['values']
            if any(isinstance(value, str) and search_text in value.lower() for value in values):
                self.packet_tree.selection_add(item)
                self.packet_tree.move(item, '', '0')
                self.packet_tree.see(item)


root = Tk()
app = App(root)
root.mainloop()
