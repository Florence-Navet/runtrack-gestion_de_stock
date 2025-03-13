from tkinter import *
import tkinter.ttk as ttk  # Importer ttk pour utiliser Combobox
from mangaStore import MangaStore

# Fenêtre principale
window = Tk()

# Personnaliser la fenêtre principale
window.title("My MangaStore")
window.geometry("1080x720")
window.minsize(480, 360)
window.iconbitmap("assets/logo.ico")
window.config(background='#ab7e9c')

# Créer la frame principale
frame_main = Frame(window, bg='#ab7e9c', bd='1', relief=SUNKEN)

# Ajouter un premier titre
label_title = Label(frame_main, text="Bienvenue dans ma boutique", font=("Courier", 25), bg='#ab7e9c', fg='#FFFFFF')
label_title.pack()

# Ajouter un sous-titre
label_subtitle = Label(frame_main, text="MANGASTORE", font=("Courier", 35), bg='#ab7e9c', fg='#FFFFFF')
label_subtitle.pack()

# Ajouter une image à la fenêtre principale
frame_image = Frame(frame_main, bg='#ab7e9c')
frame_image.pack(pady=20)

# Créer l'image
image_width = 300
image_height = 300
image = PhotoImage(file="assets/anime.png").zoom(35).subsample(32)  # Charger l'image
canvas = Canvas(frame_image, width=image_width, height=image_height, bg='#ab7e9c', bd=0, highlightthickness=0)
canvas.create_image(image_width / 2, image_height / 2, image=image)
canvas.image = image  # Important pour maintenir une référence à l'image
canvas.pack()

# Fonction pour afficher la boutique
def ouvrir_boutique():
    """Fonction pour afficher la boutique dans la même fenêtre.""" 
    global frame_boutique
    frame_boutique = Frame(window, bg='#ab7e9c')
    frame_main.pack_forget()  # Cacher la fenêtre principale

    # Créer une instance de MangaStore
    store = MangaStore()

    # Créer un frame pour l'image et les boutons dans la boutique
    frame_image_button = Frame(frame_boutique, bg='#ab7e9c')
    frame_image_button.pack(expand=YES, fill=BOTH)

    # Créer un frame pour l'image
    frame_image = Frame(frame_image_button, bg='#ab7e9c')
    frame_image.pack(side=LEFT, padx=20)

    # Créer l'image
    width = 300
    height = 300
    image = PhotoImage(file="assets/anime.png").zoom(35).subsample(32)  # Charger l'image
    canvas = Canvas(frame_image, width=width, height=height, bg='#ab7e9c', bd=0, highlightthickness=0)
    canvas.create_image(width / 2, height / 2, image=image)
    canvas.image = image  # Important pour maintenir une référence à l'image
    canvas.pack()

    # Créer un frame pour les boutons
    frame_buttons = Frame(frame_image_button, bg='#ab7e9c')
    frame_buttons.pack(side=RIGHT, padx=20, pady=20)

    # Fenêtre de produits
    frame_produits = Frame(frame_boutique, bg='#ab7e9c')
    frame_produits.pack(pady=30, fill=BOTH, expand=YES)
    
    # Treeview pour afficher les produits sous forme de tableau
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

    # Fonction pour afficher les produits dans le Treeview
    def afficher_produits_boutique():
        for item in treeview.get_children():
            treeview.delete(item)

        # Récupérer et afficher les produits
        produits = store.afficher_produits()  
        if produits:
            for p in produits:
                treeview.insert("", "end", values=(p[0], p[1], p[2], f"{p[3]}€", p[4], p[5]))
        else:
            treeview.insert("", "end", values=("Aucun produit trouvé", "", "", "", "", ""))

    # Créer un bouton pour afficher les produits
    bouton_afficher = Button(frame_buttons, text="Afficher les produits", command=afficher_produits_boutique, font=("Courier", 18))
    bouton_afficher.pack(pady=10)

    # Fonction pour ajouter un produit via un formulaire
    def ajouter_produit_boutique():
        def ajouter():
            # Récupérer les valeurs des champs de saisie
            name = entry_name.get()
            description = entry_description.get()
            price = float(entry_price.get())
            quantity = int(entry_quantity.get())
            category_name = category_combobox.get()  # Récupérer le nom de la catégorie

            # Trouver l'ID correspondant au nom de la catégorie sélectionnée
            category_id = next((cat[1] for cat in categories if cat[0] == category_name), None)

            # Ajouter le produit
            if category_id:
                store.ajouter_produit(name, description, price, quantity, category_id)
                afficher_produits_boutique()  # Afficher les produits après l'ajout
                ajout_fenetre.destroy()  # Fermer la fenêtre du formulaire
            else:
                print("Erreur : Catégorie non trouvée")

        # Créer une fenêtre pour saisir les informations du produit
        ajout_fenetre = Toplevel(window)
        ajout_fenetre.title("Ajouter un produit")
        ajout_fenetre.geometry("1080x720")

        # Créer les champs de saisie
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

        # Créer le combobox pour la sélection de la catégorie
        label_category = Label(ajout_fenetre, text="Sélectionner la catégorie:", font=("Consolas", 20))
        label_category.pack(pady=10)

        # Liste des catégories avec leurs ID
        categories = [
            ("Manga Shonen", 1),
            ("Manga Shojo", 2),
            ("Manga Seinen", 3),
            ("Goodies", 4),
            ("Figurines", 5)
        ]
        category_names = [cat[0] for cat in categories]

        # Créer un Combobox pour la sélection de la catégorie
        category_combobox = ttk.Combobox(ajout_fenetre, values=category_names, font=("Consolas", 20))
        category_combobox.pack(pady=10)
        category_combobox.set("Sélectionner une catégorie")  # Valeur par défaut

        # Bouton pour ajouter le produit
        bouton_ajouter = Button(ajout_fenetre, text="Ajouter", command=ajouter, font=("Consolas", 20))
        bouton_ajouter.pack(pady=20)

    # Ajouter un bouton pour ajouter un produit
    bouton_ajouter_produit = Button(frame_buttons, text="Ajouter un produit", command=ajouter_produit_boutique, font=("Courier", 18))
    bouton_ajouter_produit.pack(pady=10)

    # Ajouter un bouton pour revenir à la fenêtre principale
    def revenir_main_window():
        frame_boutique.pack_forget()  # Masquer la fenêtre boutique
        frame_main.pack(expand=YES)   # Afficher la fenêtre principale
        
    bouton_retour = Button(frame_buttons, text="Retour", command=revenir_main_window, font=("Courier", 18))
    bouton_retour.pack(pady=10)

    # Afficher la boutique
    frame_boutique.pack(expand=YES, fill=BOTH)

# Fenêtre principale: Ajouter un bouton
fenetre_button = Button(frame_main, text="Découvrir boutique", font=("Courier", 18), bg='#FFFFFF', fg='#ab7e9c', command=ouvrir_boutique)
fenetre_button.pack(side=TOP, pady=10, fill=X)

# Fenêtre principale: Ajouter la frame dans la fenêtre
frame_main.pack(expand=YES)

# Afficher la fenêtre principale
window.mainloop()
