import tkinter as tk
from tkinter import ttk
from tkinter import messagebox



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
    ip1 = entry_ip1.get()
    ip2 = entry_ip2.get()

    try:
        ip_list = generate_ip_list(ip1, ip2)
        count = len(ip_list)
        tree.delete(*tree.get_children())
        for ip in ip_list:
            tree.insert('', 'end', values=(ip,))
      
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer des adresses IP valides.")

# Create the main window
root = tk.Tk()
root.title("Calculateur d'adresses IP")

# Create and place widgets
label_ip1 = tk.Label(root, text="Première adresse IP:")
label_ip1.grid(row=0, column=0, padx=5, pady=5, sticky="e")

entry_ip1 = tk.Entry(root)
entry_ip1.grid(row=0, column=1, padx=5, pady=5)

label_ip2 = tk.Label(root, text="Deuxième adresse IP:")
label_ip2.grid(row=1, column=0, padx=5, pady=5, sticky="e")

entry_ip2 = tk.Entry(root)
entry_ip2.grid(row=1, column=1, padx=5, pady=5)

button_calculate = tk.Button(root, text="Calculer", command=calculate_ips)
button_calculate.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Create Treeview for displaying IP addresses
tree = ttk.Treeview(root, columns=('IP Address',), show='headings')
tree.heading('IP Address', text='Adresse IP')
tree.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Run the Tkinter event loop
root.mainloop()
