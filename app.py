from tkinter import *
import tkinter.ttk as ttk  # Importer ttk pour utiliser Treeview
from mangaStore import MangaStore

# Fenêtre 1: Créer la fenêtre principale
window = Tk()

# Personnaliser cette fenêtre
window.title("My MangaStore")
window.geometry("1080x720")
window.minsize(480, 360)
window.iconbitmap("assets/logo.ico")
window.config(background='#ab7e9c')

# Création de l'image
width = 300
height = 300
image = PhotoImage(file="assets/anime.png").zoom(35).subsample(32)
canvas = Canvas(window, width=width, height=height, bg='#ab7e9c', bd=0, highlightthickness=0)
canvas.create_image(width / 2, height / 2, image=image)
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
    """Fonction pour ouvrir une nouvelle fenêtre (Fenêtre 2)."""
    # Fenêtre 2: Créer une nouvelle fenêtre
    nouvelle_fenetre = Toplevel()
    nouvelle_fenetre.title("Nouvelle Boutique")
    nouvelle_fenetre.geometry("1080x720")

    # Créer une instance de MangaStore dans la nouvelle fenêtre
    store = MangaStore()

    # Fenêtre 2: Frame pour afficher les produits
    frame_produits = Frame(nouvelle_fenetre)
    frame_produits.pack(pady=30, fill=BOTH, expand=YES)  # Ajout de 'fill=BOTH' et 'expand=YES'

    # Fenêtre 2: Treeview pour afficher les produits sous forme de tableau
    columns = ('ID', 'Nom', 'Description', 'Prix', 'Stock', 'Catégorie')
    treeview = ttk.Treeview(frame_produits, columns=columns, show='headings')
    treeview.pack(fill=BOTH, expand=YES)

    # Définir les en-têtes des colonnes
    for col in columns:
        treeview.heading(col, text=col)

    # Définir la largeur des colonnes
    treeview.column('ID', width=80)          # Colonne ID plus petite
    treeview.column('Nom', width=200)        # Colonne Nom
    treeview.column('Description', width=300)# Colonne Description
    treeview.column('Prix', width=100)       # Colonne Prix plus petite
    treeview.column('Stock', width=100)      # Colonne Stock plus petite
    treeview.column('Catégorie', width=150)  # Colonne Catégorie plus petite

    # Fenêtre 2: Fonction pour afficher les produits dans le Treeview
    def afficher_produits_boutique():
        # Effacer les produits existants dans le Treeview avant d'ajouter les nouveaux
        for item in treeview.get_children():
            treeview.delete(item)

        # Récupérer et afficher les produits
        produits = store.afficher_produits()  # On récupère les produits depuis la base de données
        if produits:
            for p in produits:
                # Ajouter chaque produit dans le Treeview
                treeview.insert("", "end", values=(p[0], p[1], p[2], f"{p[3]}€", p[4], p[5]))
        else:
            treeview.insert("", "end", values=("Aucun produit trouvé", "", "", "", "", ""))

    # Fenêtre 2: Fonction pour ajouter un produit via un formulaire
    def ajouter_produit_boutique():
        def ajouter():
            # Récupérer les valeurs des champs de saisie
            name = entry_name.get()
            description = entry_description.get()
            price = float(entry_price.get())
            quantity = int(entry_quantity.get())
            category_id = int(entry_category.get())

            # Ajouter le produit
            store.ajouter_produit(name, description, price, quantity, category_id)

            # Fermer la fenêtre du formulaire
            ajout_fenetre.destroy()

        # Fenêtre 3: Créer une fenêtre pour saisir les informations du produit
        ajout_fenetre = Toplevel(nouvelle_fenetre)
        ajout_fenetre.title("Ajouter un produit")
        ajout_fenetre.geometry("720x450")

        # Créer les champs de saisie avec la police Consolas et taille de police plus grande
        label_name = Label(ajout_fenetre, text="Nom du produit:", font=("Consolas", 20))
        label_name.pack(pady=10)
        entry_name = Entry(ajout_fenetre, font=("Consolas", 20))
        entry_name.pack(pady=10)

        label_description = Label(ajout_fenetre, text="Description du produit:", font=("Consolas", 20))
        label_description.pack(pady=10)
        entry_description = Entry(ajout_fenetre, font=("Consolas", 20))
        entry_description.pack(pady=10)

        label_price = Label(ajout_fenetre, text="Prix:", font=("Consolas", 20))
        label_price.pack(pady=10)
        entry_price = Entry(ajout_fenetre, font=("Consolas", 20))
        entry_price.pack(pady=10)

        label_quantity = Label(ajout_fenetre, text="Quantité:", font=("Consolas", 20))
        label_quantity.pack(pady=10)
        entry_quantity = Entry(ajout_fenetre, font=("Consolas", 20))
        entry_quantity.pack(pady=10)

        label_category = Label(ajout_fenetre, text="ID de la catégorie:", font=("Consolas", 20))
        label_category.pack(pady=10)
        entry_category = Entry(ajout_fenetre, font=("Consolas", 20))
        entry_category.pack(pady=10)

        # Bouton pour ajouter le produit avec police Consolas et taille plus grande
        bouton_ajouter = Button(ajout_fenetre, text="Ajouter", command=ajouter, font=("Consolas", 20))
        bouton_ajouter.pack(pady=20)

    # Fenêtre 2: Création du menu
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

# Fenêtre 1: Ajouter un premier bouton
fenetre_button = Button(frame, text="Découvrir boutique", font=("Courier", 18), bg='#FFFFFF', fg='#ab7e9c', command=ouvrir_boutique)
fenetre_button.pack(side=TOP, pady=10, fill=X)

# Fenêtre 1: Ajouter la frame dans la fenêtre principale
frame.pack(expand=YES)

# Fenêtre 1: Afficher la fenêtre principale
window.mainloop()
