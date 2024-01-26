import tkinter
import tkinter.messagebox
import customtkinter
import netifaces
import subprocess
from tkinter import filedialog
import sys
from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget


customtkinter.set_default_color_theme("green")


# Récupération des interfaces 
interfacelist=netifaces.interfaces()
   
 
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("SNIFFER")
        self.geometry(f"{2000}x{2000}")

        # configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3,4,5,6,7,8), weight=3)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Sniffer", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.telecharger_contenu_textbox,text="Save")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event,text='Start')
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event,text='Stop')
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, command=self.importer_contenu_textbox,text='Import')
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, command=self.importer_contenu_textbox,text='Itest')
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
        #create textbox Numéro 
        #self.textbox0 = customtkinter.CTkTextbox(self, width=200,height=100,activate_scrollbars=False)              
        #self.textbox0.grid(row=0, column=1,rowspan=2, padx=(40, 1), pady=(50,0),sticky="nsew")
        
        
        



        # titre de la textboxNuméro
        #self.textbox0_title = customtkinter.CTkLabel(self, text="Numéro",)
        #self.textbox0_title.grid(row=0, column=1,sticky="n")
        #self.textbox0_title.grid_rowconfigure(1,weight=2)
        #create textbox Time
        #self.textbox1 = customtkinter.CTkTextbox(self, width=200,height=100,activate_scrollbars=False)                
        #self.textbox1.grid(row=0, column=2,rowspan=2, padx=(1, 0), pady=(50,0),sticky="nsew")
        # titre de la textboxTime
        #self.textbox1_title = customtkinter.CTkLabel(self, text="Time")
        #self.textbox1_title.grid(row=0, column=2,sticky="n")
        #self.textbox1_title.grid_rowconfigure(1,weight=2)
        # create textbox Ip src
        #self.textbox2= customtkinter.CTkTextbox(self, width=200,height=100,activate_scrollbars=False)                
        #self.textbox2.grid(row=0, column=3,rowspan=2, padx=(1, 0), pady=(50,0),sticky="nsew")
        # titre de la textboxipsrc
        #self.textbox2_title = customtkinter.CTkLabel(self, text="Ip source")
        #self.textbox2_title.grid(row=0, column=3,sticky="n")
        #self.textbox2_title.grid_rowconfigure(1,weight=2)
        # create textbox Ip dst
        #self.textbox3 = customtkinter.CTkTextbox(self, width=200,height=100,activate_scrollbars=False,)                
        #self.textbox3.grid(row=0, column=4,rowspan=2, padx=(1, 0), pady=(50,0),sticky="nsew")
        # titre de la textboxipdst
        #self.textbox3_title = customtkinter.CTkLabel(self, text="Ip destination")
        #self.textbox3_title.grid(row=0, column=4,sticky="n")
        #self.textbox3_title.grid_rowconfigure(1,weight=2)
        # create textox info
        #self.textbox4 = customtkinter.CTkTextbox(self, width=200,height=100)                
        #self.textbox4.grid(row=0, column=5,rowspan=2, padx=(1, 0), pady=(50,0),sticky="nsew")
        # titre create textox infoitem_double_cl
        #self.textbox4_title = customtkinter.CTkLabel(self, text="info")
        #self.textbox4_title.grid(row=0, column=5,sticky="n")
        #self.textbox4_title.grid_rowconfigure(1,weight=1)
        

        #self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, orientation="vertical")
        #self.slider_2.grid(row=0, column=6, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns")
        
        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=180)
        self.tabview.grid(row=0, column=8, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.tabview.add("Interfaces")
        self.tabview.tab("Interfaces").grid_columnconfigure(0, weight=3)  # configure grid of individual tabs
               
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Interfaces"), dynamic_resizing=False, values=interfacelist)  
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
            
        #self.string_input_button = customtkinter.CTkButton(self.tabview.tab("CTkTabview"), text="Open CTkInputDialog",
        #                                                   command=self.open_input_dialog_event)
        #self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        
 
        # create checkbox and switch frame
        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=1, column=8, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text='Serveur 1')
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text='Serveur 2')
        self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text='Serveur 3')
        self.checkbox_3.grid(row=3, column=0, pady=(20,0), padx=20, sticky="n")
        self.checkbox_4 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text='Serveur 4')
        self.checkbox_4.grid(row=4, column=0, pady=(20,0), padx=20, sticky="n")
        self.checkbox_5 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text='Serveur 5')
        self.checkbox_5.grid(row=5, column=0, pady=(20,0), padx=20, sticky="n")
        self.checkbox_6 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text='Serveur 6')
        self.checkbox_6.grid(row=6, column=0, pady=(20,0), padx=20, sticky="n")
        self.checkbox_7 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text='Serveur 7')
        self.checkbox_7.grid(row=7, column=0, pady=(20,0), padx=20, sticky="n")
        # Bouton nouvelle page 
        self.checkbox_8 = customtkinter.CTkButton(self.checkbox_slider_frame, text='Nouvelle page',command=self.sidebar_button_event)
        #executer_script('/home/test/sae501/App/apptestpage2.py'
        self.checkbox_8 .grid(row=8, column=0, padx=(20,0), pady=20)
        

        #set default values 
        self.sidebar_button_3.configure(state="disabled")
        self.checkbox_4.configure(state="disabled")
        #self.sidebar_button_3.configure(state="disabled")
        self.checkbox_5.configure(state="disabled")
        #self.sidebar_button_6.configure(state="disabled")
        self.checkbox_6.configure(state="disabled")
        #self.sidebar_button_7.configure(state="disabled")
        self.checkbox_7.configure(state="disabled")
        #self.checkbox_1.select()
        self.checkbox_7.configure(state="disabled")
        # Settings de base 
        #self.appearance_mode_optionemenu.set("Dark")
        #self.scaling_optionemenu.set("100%")
        #self.optionmenu_1.set("Sélectionnnez")
        #paquet = {'Type': 'DHCPREQUEST', 'Ether': {'dst': 'ff:ff:ff:ff:ff:ff', 'src': 'b0:7b:25:26:a1:19', 'type': 2048}, 'IP': {'version': 4, 'src': '0.0.0.0', 'dst': '255.255.255.255', 'ttl': 128}, 'DHCP': {'options': ('client_id', b'\x01\xb0{%&\xa1J')}, 'UDP': {'sport': 68, 'dport': 67, 'len': 308}, 'BOOTP': {'ciaddr': '0.0.0.0', 'yiaddr': '0.0.0.0', 'siaddr': '0.0.0.0', 'giaddr': '0.0.0.0', 'chaddr': b'\xb0{%&\xa1\x19\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'}}
        #type = paquet['Type']
        #ip_source = paquet['IP']['src']
        #ip_dest = paquet['IP']['dst']
        # textbox valeur à afficher
        #self.textbox0.insert("0.1", "Voici le numéro du paquet  \n\n"* 100)
    
        #self.textbox0.insert("0.1"," \n\n"* 100)
  
        #self.textbox1.insert("0.1", ""+ type+" \n\n" * 100)
        #self.textbox2.insert("0.1", ""+ ip_source +"\n\n" * 100)
        #self.textbox3.insert("0.1", ""+ ip_dest +"\n\n" * 100)
        #self.textbox4.insert("0.1", "Voici des informations\n\n" * 100)
        #self.fenetre_principale = QWidget()
        #layout = QVBoxLayout(self.fenetre_principale)

        #self.packet_tree = QTreeWidget(self.fenetre_principale)
        #self.packet_tree.setHeaderLabels(['ID', 'IP SRC', 'IP DST', 'INFO'])

        
        #self.seg_button_1.configure(values=["Numéro", "Time", "src","dst","protocol","lenght","info"])
        #self.seg_button_1.set("Value 2")

    #def open_input_dialog_event(self):
    #    dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
    #    print("CTkInputDialog:", dialog.get_input())
    
    # Changement de l'apparance
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    #Changement du scaling 
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
    
    # Action sur la side bar
    def sidebar_button_event(self):
        print("sidebar_button click")
            
    #def newpage2(self):
        
        #subprocess.run('python3 -m venv venv')
        #subprocess.run('source venv/bin/activate')
        #subprocess.run('pip3 install tk')
        #subprocess.run('pip3 install customtkinter')
    #try:
        #subprocess.run(['python3 $HOME/sae501/App/apptestpage2.py'], check=True)
    #except subprocess.CalledProcessError as e:
        #print(f"Erreur du chargement de la page : {e}")


    def telecharger_contenu_textbox(self):
        try:
            # Obtenir le contenu du widget Text
            contenu_texte = self.textbox.get("1.0", "end-1c")

            # Ouvrir une boîte de dialogue pour choisir l'emplacement de sauvegarde
            fichier_destination = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Fichiers texte", "*.txt")])

            # Vérifier si l'utilisateur a sélectionné un emplacement
            if fichier_destination:
                # Écrire le contenu dans le fichier texte
                with open(fichier_destination, 'w') as fichier:
                    fichier.write(contenu_texte)
                print(f"Le contenu a été sauvegardé avec succès dans le fichier : {fichier_destination}")
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")

    def importer_contenu_textbox(self):
        try:
            # Ouvrir une boîte de dialogue pour choisir le fichier à importer
            fichier_source = filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt")])

            # Vérifier si l'utilisateur a sélectionné un fichier
            if fichier_source:
                # Lire le contenu du fichier texte
                with open(fichier_source, 'r') as fichier:
                    contenu_texte = fichier.read()

                # Insérer le contenu dans le widget Text
                self.textbox.delete("1.0", "end-1c")  # Effacer le contenu existant
                self.textbox.insert("1.0", contenu_texte)  # Insérer le nouveau contenu
                print(f"Le contenu a été importé avec succès depuis le fichier : {fichier_source}")
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")
    

if __name__ == "__main__":
    app = App()
    app.mainloop()







