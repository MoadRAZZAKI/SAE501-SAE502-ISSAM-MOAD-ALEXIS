import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter

customtkinter.set_default_color_theme("green")
customtkinter.set_appearance_mode("dark")

# Les fonctions utilitaires restent inchangées

def calculate_ips_tab():
    global ip_list
    global v
    ip1 = entry_ip1_tab.get()
    ip2 = entry_ip2_tab.get()

    try:
        ip_list = generate_ip_list(ip1, ip2)
        v = len(ip_list)
       
        count = len(ip_list)
        pourcent = round(count * 100 / v, 1)
        label_count_tab.configure(text=f" Pourcentage: {pourcent}%")
        tree_tab.delete(*tree_tab.get_children())
        for ip in ip_list:
            tree_tab.insert('', 'end', values=(ip,))
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer des adresses IP valides.")

def remove_temporarily_tab():
    ip_to_remove = entry_remove_ip_tab.get()
    temporary_remove_ip(ip_to_remove)

root = customtkinter.CTk()
root.title("Config serveur")

label_ip1 = customtkinter.CTkLabel(root, text="Première adresse IP:")
label_ip1.grid(row=0, column=0, padx=5, pady=5, sticky="e")

entry_ip1_tab = customtkinter.CTkEntry(root)
entry_ip1_tab.grid(row=0, column=1, padx=5, pady=5)

label_ip2 = customtkinter.CTkLabel(root, text="Deuxième adresse IP:")
label_ip2.grid(row=1, column=0, padx=5, pady=5, sticky="e")

entry_ip2_tab = customtkinter.CTkEntry(root)
entry_ip2_tab.grid(row=1, column=1, padx=5, pady=5)

button_calculate_tab = customtkinter.CTkButton(root, text="Calculer", command=calculate_ips_tab)
button_calculate_tab.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

notebook = customtkinter.CTkTabview(root, width=250)
notebook.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

frame_tab = notebook.add("Serveur status")
frame_tab.grid_columnconfigure(0, weight=1)
frame_tab.grid_rowconfigure(0, weight=1)

tree_tab = ttk.Treeview(frame_tab, columns=('IP Address',), show='headings')
tree_tab.heading('IP Address', text='Adresse IP')
tree_tab.grid(row=0, column=0, padx=5, pady=5)

label_remove_ip_tab = customtkinter.CTkLabel(root, text="Adresse IP à supprimer temporairement:")
label_remove_ip_tab.grid(row=4, column=0, padx=5, pady=5, sticky="e")

entry_remove_ip_tab = customtkinter.CTkEntry(root)
entry_remove_ip_tab.grid(row=4, column=1, padx=5, pady=5)

button_remove_temporarily_tab = customtkinter.CTkButton(root, text="Supprimer temporairement", command=remove_temporarily_tab)
button_remove_temporarily_tab.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

label_count_tab = customtkinter.CTkLabel(root, text="Pourcentage: 0 %")
label_count_tab.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
