import customtkinter as ctk 


#fenetre 
fenetre= ctk.CTk()
fenetre.title('App')
fenetre.geometry('7000x7000')

#widget 
titre = ctk.CTkLabel(fenetre,
                    text ='Label custom ',
                    fg_color ='black',
                    text_color = 'white',
                    corner_radius= 10
                    )           
titre.pack()

button = ctk.CTkButton(fenetre,
                        text = 'Light Mode',
                        fg_color= ('Black','white'),
                        text_color='red',
                        corner_radius= 15 ,
                        hover_color= 'orange',
                        command = lambda: ctk.set_appearance_mode('light')
                        )
button.pack()
button = ctk.CTkButton(fenetre,
                        text = 'Darkmode',
                        fg_color= ('white','black'),
                        text_color='red',
                        corner_radius= 15 ,
                        hover_color= 'orange',
                        command = lambda: ctk.set_appearance_mode('Dark')
                        )
button.pack()

fenetre.mainloop()