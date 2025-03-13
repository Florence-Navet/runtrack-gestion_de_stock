from tkinter import *

#creer une premier fenetre
window = Tk()


#personnaliser cette fenetre
window.title("My MangaStore")
window.geometry("720x480")
window.minsize(480,360)
window.iconbitmap("assets/logo.ico")
window.config(background='#ab7e9c')

#creation de la frame
frame = Frame(window, bg='#ab7e9c', bd='1', relief=SUNKEN)

#ajouter du premier titre
label_title = Label(frame, text="Bienvenue dans ma boutique", font=("Courier", 30), bg='#ab7e9c', fg='#FFFFFF')
# label_title.pack(side=LEFT)
label_title.pack()

#ajouter un sous-titre
label_subtitle = Label(frame, text="MANGASTORE", font=("Courier", 40), bg='#ab7e9c', fg='#FFFFFF')
# label_title.pack(side=LEFT)
label_subtitle.pack()


#ajouter un premier bouton
yt_button = 

#ajouter
frame.pack(expand=YES)

#afficher
window = mainloop()