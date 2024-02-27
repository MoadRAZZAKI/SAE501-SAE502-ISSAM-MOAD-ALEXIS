import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter

customtkinter.set_default_color_theme("green")
customtkinter.set_appearance_mode("dark")

def ip_to_int(ip_address):
    octets = ip_address.split('.')
    return int(octets[0]) * 256 ** 3 + int(octets[1]) * 256 ** 2 + int(octets[2]) * 256 + int(octets[3])

def int_to_ip(int_address):
    return '.'.join(str((int_address >> i) & 0xFF) for i in (24, 16, 8, 0))

def generate_ip_list(ip1, ip2):
    ip_list = []
    ip1_int = ip_to_int(ip1)
    ip2_int = ip_to_int(ip2)

    start_ip = min(ip1_int, ip2_int)
    end_ip = max(ip1_int, ip2_int)

    for i in range(start_ip, end_ip + 1):
        ip_list.append(int_to_ip(i))

    return ip_list

def calculate_ips():
    global ip_list
    global v
    ip1 = entry_ip1.get()
    ip2 = entry_ip2.get()

    try:
        ip_list = generate_ip_list(ip1, ip2)
        v = len(ip_list)
        
        count = len(ip_list)
        pourcentage = round(count * 100 / v, 1)
        label_count.configure(text=f"Pourcentage: {pourcentage}%")
        tree.delete(*tree.get_children())
        for ip in ip_list:
            tree.insert('', 'end', values=(ip,))
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer des adresses IP valides.")

def temporary_remove_ip(ip_to_remove):
    global ip_list
    for item in tree.get_children():
        if tree.item(item)['values'][0] == ip_to_remove:
            tree.delete(item)
            ip_list.remove(ip_to_remove)
            
            count = len(ip_list)
            pourcentage = round(count * 100 / v, 1)
            label_count.configure(text=f"Pourcentage: {pourcentage}%")
            
            root.after(10000, lambda: restore_ip(ip_to_remove))
            break

def restore_ip(ip_to_restore):
    global ip_list
    ip_list.append(ip_to_restore)
    count = len(ip_list)
    pourcentage = round(count * 100 / v, 1)
    label_count.configure(text=f"Pourcentage: {pourcentage}%")
    tree.insert('', 'end', values=(ip_to_restore,))

def remove_temporarily():
    ip_to_remove = entry_remove_ip.get()
    temporary_remove_ip(ip_to_remove)

def plot_pie_chart():
    global ip_list
    global v

    # Calcul du pourcentage des adresses IP disponibles
    count = len(ip_list)
    pourcentage = round(count * 100 / v, 1)

    # Création du camembert
    labels = ['Disponible', 'Non Disponible']
    sizes = [pourcentage, 100 - pourcentage]

    if pourcentage < 15 and pourcentage >= 1 :
        messagebox.showwarning("Attention", "Il y a moins de 15% d'adresses IP disponibles.")
    elif pourcentage < 1:
        messagebox.showwarning("Attention", "Il n'y a plus d'adresses IP disponibles.")

    figure = Figure(figsize=(5, 5), dpi=100)
    plot = figure.add_subplot(1, 1, 1)
    plot.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plot.axis('equal')

    # Affichage du camembert dans une fenêtre Tkinter
    pie_window = tk.Toplevel()
    pie_window.title("Camembert des adresses IP disponibles")
    canvas = FigureCanvasTkAgg(figure, pie_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

first_10_removed_ips = []

def remove_first_10_ips_temporarily():
    global ip_list
    global v
    global first_10_removed_ips

    # Suppression des 10 premières adresses IP de la liste
    for _ in range(10):
        if ip_list:
            ip_to_remove = ip_list.pop(0)
            first_10_removed_ips.append(ip_to_remove)
            count = len(ip_list)
            pourcentage = round(count * 100 / v, 1)
            label_count.configure(text=f"Pourcentage: {pourcentage}%")
            tree.delete(tree.get_children()[0])  # Supprimer la première adresse de l'arbre

    # Rétablissement des adresses IP après 10 secondes
    root.after(10000, restore_first_10_ips)

def restore_first_10_ips():
    global ip_list
    global v
    global first_10_removed_ips

    # Ajout des 10 premières adresses IP précédemment supprimées
    for ip_to_restore in first_10_removed_ips:
        ip_list.append(ip_to_restore)
        count = len(ip_list)
        pourcentage = round(count * 100 / v, 1)
        label_count.configure(text=f"Pourcentage: {pourcentage}%")
        tree.insert('', 'end', values=(ip_to_restore,))
    
    # Effacer la liste des 10 premières adresses IP retirées
    first_10_removed_ips = []

# Création de la fenêtre principale
root = customtkinter.CTk()
root.title("Config serveur")

# Widgets pour les adresses IP
label_ip1 = customtkinter.CTkLabel(root, text="Première adresse IP:")
label_ip1.grid(row=0, column=0, padx=5, pady=5, sticky="e")

entry_ip1 = customtkinter.CTkEntry(root)
entry_ip1.grid(row=0, column=1, padx=5, pady=5)

label_ip2 = customtkinter.CTkLabel(root, text="Deuxième adresse IP:")
label_ip2.grid(row=1, column=0, padx=5, pady=5, sticky="e")

entry_ip2 = customtkinter.CTkEntry(root)
entry_ip2.grid(row=1, column=1, padx=5, pady=5)

button_calculate = customtkinter.CTkButton(root, text="Calculer", command=calculate_ips)
button_calculate.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Treeview pour afficher les adresses IP
tree = ttk.Treeview(root, columns=('IP Address',), show='headings')
tree.heading('IP Address', text='Adresse IP')
tree.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Widgets pour la suppression temporaire
label_remove_ip = customtkinter.CTkLabel(root, text="Adresse IP à supprimer temporairement:")
label_remove_ip.grid(row=4, column=0, padx=5, pady=5, sticky="e")

entry_remove_ip = customtkinter.CTkEntry(root)
entry_remove_ip.grid(row=4, column=1, padx=5, pady=5)

button_remove_temporarily = customtkinter.CTkButton(root, text="Supprimer temporairement", command=remove_temporarily)
button_remove_temporarily.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Label pour afficher le pourcentage
label_count = customtkinter.CTkLabel(root, text="Pourcentage: 0 %")
label_count.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

# Bouton pour afficher le camembert
button_plot_pie_chart = customtkinter.CTkButton(root, text="Afficher le camembert", command=plot_pie_chart)
button_plot_pie_chart.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

# Bouton pour supprimer temporairement les 10 premières adresses IP
button_remove_first_10_ips = customtkinter.CTkButton(root, text="Supprimer les 10 premières IP", command=remove_first_10_ips_temporarily)
button_remove_first_10_ips.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

# Lancement de la boucle principale Tkinter
root.mainloop()
