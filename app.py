from tkinter import *
import tkinter as tk

# Créer la fenêtre principale
window = Tk()

# Personnaliser cette fenêtre
window.title("My MangaStore")
window.geometry("720x480")
window.minsize(480,360)
window.iconbitmap("assets/logo.ico")
window.config(background='#ab7e9c')

#creation, d'image
width = 300
height = 300
image = PhotoImage(file="assets/anime.png").zoom(35).subsample(32)
canvas = Canvas(window, width=width, height=height, bg='#ab7e9c', bd = 0, highlightthickness=0)
canvas.create_image(width/2, height/2, image=image)
canvas.pack(expand=YES)

# Création de la frame
frame = Frame(window, bg='#ab7e9c', bd='1', relief=SUNKEN)

# Ajouter un premier titre
label_title = Label(frame, text="Bienvenue dans ma boutique", font=("Courier", 25), bg='#ab7e9c', fg='#FFFFFF')
label_title.pack()

# Ajouter un sous-titre
label_subtitle = Label(frame, text="MANGASTORE", font=("Courier", 35), bg='#ab7e9c', fg='#FFFFFF')
label_subtitle.pack()


def ouvrir_boutique():
    """Fonction pour ouvrir une nouvelle fenêtre."""
    # Créer une nouvelle fenêtre
    nouvelle_fenetre = Toplevel()
    nouvelle_fenetre.title("Nouvelle Boutique")
    nouvelle_fenetre.geometry("720x480")
    
    # Ajouter un label dans la nouvelle fenêtre
    label = Label(nouvelle_fenetre, text="Bienvenue dans notre boutique !", font=("Courier", 15))
    label.pack(pady=50)


# Ajouter un premier bouton
fenetre_button = Button(frame, text="Découvrir boutique", font=("Courier", 18), bg='#FFFFFF', fg='#ab7e9c', command=ouvrir_boutique)
fenetre_button.pack(side=TOP, pady=10, fill=X)

# Ajouter la frame dans la fenêtre principale
frame.pack(expand=YES)

# Afficher la fenêtre principale
window.mainloop()
