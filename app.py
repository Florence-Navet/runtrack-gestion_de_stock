from tkinter import *
import tkinter as tk
from mangaStore import MangaStore

# Créer la fenêtre principale
window = Tk()

# Personnaliser cette fenêtre
window.title("My MangaStore")
window.geometry("720x480")
window.minsize(480, 360)
window.iconbitmap("assets/logo.ico")
window.config(background='#ab7e9c')

# création, d'image
width = 300
height = 300
image = PhotoImage(file="assets/anime.png").zoom(35).subsample(32)
canvas = Canvas(window, width=width, height=height, bg='#ab7e9c', bd=0, highlightthickness=0)
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

    # Créer une instance de MangaStore dans la nouvelle fenêtre
    store = MangaStore()

    # Frame pour afficher les produits
    frame_produits = Frame(nouvelle_fenetre)
    frame_produits.pack(pady=20)

    # Liste pour afficher les produits
    listbox = Listbox(frame_produits, width=80, height=15)
    listbox.pack()

    # Fonction pour afficher les produits dans la Listbox
    def afficher_produits_boutique():
        # Effacer les produits existants dans la Listbox avant d'ajouter les nouveaux
        listbox.delete(0, END)

        # Récupérer et afficher les produits
        produits = store.afficher_produits()  # On récupère les produits depuis la base de données
        if produits:
            for p in produits:
                # Formatage des produits et ajout dans la Listbox
                listbox.insert(END, f"ID: {p[0]} | Nom: {p[1]} | Description: {p[2]} | Prix: {p[3]}€ | Stock: {p[4]} | Catégorie: {p[5]}")
        else:
            listbox.insert(END, "Aucun produit trouvé.")

    # Fonction pour ajouter un produit
    def ajouter_produit_boutique():
        # Tu peux ajouter des champs pour que l'utilisateur saisisse les informations du produit
        name = "Nom du produit"
        description = "Description du produit"
        price = 10.0
        quantity = 5
        category_id = 1
        store.ajouter_produit(name, description, price, quantity, category_id)

    # Création du menu
    menu_bar = Menu(nouvelle_fenetre)

    # Menu Fichier
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Afficher les produits", command=afficher_produits_boutique)
    file_menu.add_command(label="Ajouter un produit", command=ajouter_produit_boutique)
    file_menu.add_command(label="Quitter", command=nouvelle_fenetre.quit)
    menu_bar.add_cascade(label="Fichier", menu=file_menu)

    # Afficher la barre de menu
    nouvelle_fenetre.config(menu=menu_bar)

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
