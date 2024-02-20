import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
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
        v =len(ip_list)
       
        count = len(ip_list)
        pourcent=round(count*100/v,1)
        label_count.configure(text=f" Pourcentage: {pourcent}%")
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
            pourcent=round(count*100/v,1)
            print (pourcent)
            label_count.configure(text=f"Pourcentage: {pourcent}%")
            
            root.after(10000, lambda: restore_ip(ip_to_remove))
            break

def restore_ip(ip_to_restore):
    global ip_list
    
    
    ip_list.append(ip_to_restore)
    count = len(ip_list)
    pourcent=round(count*100/v,1)
    label_count.configure(text=f"Pourcentage: {pourcent}%")
    tree.insert('', 'end', values=(ip_to_restore,))

def remove_temporarily():
    ip_to_remove = entry_remove_ip.get()
    temporary_remove_ip(ip_to_remove)

# Create the main window
root = customtkinter.CTk()
root.title("Config serveur")

# Create and place widgets
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

# Create Treeview for displaying IP addresses
tree = ttk.Treeview(root, columns=('IP Address',), show='headings')
tree.heading('IP Address', text='Adresse IP')
tree.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Create and place widgets for temporary removal
label_remove_ip =customtkinter.CTkLabel(root, text="Adresse IP à supprimer temporairement:")
label_remove_ip.grid(row=4, column=0, padx=5, pady=5, sticky="e")

entry_remove_ip = customtkinter.CTkEntry(root)
entry_remove_ip.grid(row=4, column=1, padx=5, pady=5)

button_remove_temporarily = customtkinter.CTkButton(root, text="Supprimer temporairement", command=remove_temporarily)
button_remove_temporarily.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Label to display the size of the list
label_count = customtkinter.CTkLabel(root, text="Pourcentage: 0 %")
label_count.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

# Run the Tkinter event loop
root.mainloop()
