import tkinter as tk
from tkinter import ttk
import customtkinter
#import netifaces
import subprocess
from tkinter import filedialog
import time
import csv
import psutil
from sniffer import *
from sniffer import lancement_sniffing
from sniffer import traitement_paquet
#from sniffer import watch_collection
import time
from tkinter import messagebox
#import motor.motor_asyncio
from pymongo import MongoClient, change_stream
import asyncio
import json



customtkinter.set_default_color_theme("green")
customtkinter.set_appearance_mode("dark") 
interfacelist = [interface for interface in psutil.net_if_addrs().keys()]#netifaces.interfaces()
# Récupération des interfaces


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.sniffer = None
        self.compteur = 0 #TEST
        self.taille = 0
        self.selected_value = None
        self.started = False

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
