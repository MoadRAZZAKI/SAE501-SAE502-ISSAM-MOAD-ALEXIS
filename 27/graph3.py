import tkinter as tk
from tkinter import messagebox
import customtkinter

class YourApplication(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        
        
        self.search_entry = customtkinter.CTkEntry(self)
        self.search_entry.bind("<Return>", self.search1)
        self.search_entry.grid(row=0, column=0, padx=10, pady=10)

        self.alerte_label = customtkinter.CTkLabel(self, text="Adresse du DHCP", font=("Arial", 12))
        self.alerte_label.grid(row=1, column=0, padx=10, pady=(80, 0), sticky="nw")

    def search1(self, event):
        # Récupérer la valeur de l'Entry
        search_text = self.search_entry.get()

        # Mettre à jour le texte de l'étiquette
        self.alerte_label.config(text=search_text)

if __name__ == "__main__":
    app = YourApplication()
    app.mainloop()