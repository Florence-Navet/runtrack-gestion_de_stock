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
label_title = Label(frame_main, text="Gestion de ma boutique", font=("Courier", 25), bg='#ab7e9c', fg='#FFFFFF')
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
    def afficher_produits_boutique(categorie=None):
        for item in treeview.get_children():
            treeview.delete(item)

        # Récupérer et afficher les produits filtrés par catégorie si nécessaire
        produits = store.filtrer_produits_par_categorie(categorie) if categorie else store.afficher_produits()
        if produits:
            for p in produits:
                treeview.insert("", "end", values=(p[0], p[1], p[2], f"{p[3]}€", p[4], p[5]))
        else:
            treeview.insert("", "end", values=("Aucun produit trouvé", "", "", "", "", ""))

    # Combobox pour filtrer par catégorie
    def appliquer_filtre():
        category_name = category_combobox.get()
        afficher_produits_boutique(category_name)

    # Liste des catégories disponibles
    categories = [
        ("Manga Shonen", 1),
        ("Manga Shojo", 2),
        ("Manga Seinen", 3),
        ("Goodies", 4),
        ("Figurines", 5)
    ]
    category_names = [cat[0] for cat in categories]

    # Créer un Combobox pour la sélection de la catégorie
    label_category = Label(frame_buttons, text="Filtrer par catégorie:", font=("Consolas", 20), bg='#ab7e9c')
    label_category.pack(pady=10)

    category_combobox = ttk.Combobox(frame_buttons, values=category_names, font=("Consolas", 20))
    category_combobox.pack(pady=10)
    category_combobox.set("Sélectionner une catégorie")  # Valeur par défaut

    # Bouton pour appliquer le filtre
    bouton_filtrer = Button(frame_buttons, text="Appliquer le filtre", command=appliquer_filtre, font=("Courier", 18))
    bouton_filtrer.pack(pady=10)

    # Créer un bouton pour afficher tous les produits
    bouton_afficher_tous = Button(frame_buttons, text="Afficher tous les produits", command=lambda: afficher_produits_boutique(), font=("Courier", 18))
    bouton_afficher_tous.pack(pady=10)

    # Ajout d'un produit
    def ajouter_produit_window():
        """Fonction pour ajouter un produit"""
        add_window = Toplevel(window)
        add_window.title("Ajouter un produit")
        add_window.geometry("400x400")

        # Champs pour les informations du produit
        label_name = Label(add_window, text="Nom du produit:", font=("Consolas", 14))
        label_name.pack(pady=5)
        entry_name = Entry(add_window, font=("Consolas", 14))
        entry_name.pack(pady=5)

        label_desc = Label(add_window, text="Description du produit:", font=("Consolas", 14))
        label_desc.pack(pady=5)
        entry_desc = Entry(add_window, font=("Consolas", 14))
        entry_desc.pack(pady=5)

        label_price = Label(add_window, text="Prix du produit:", font=("Consolas", 14))
        label_price.pack(pady=5)
        entry_price = Entry(add_window, font=("Consolas", 14))
        entry_price.pack(pady=5)

        label_quantity = Label(add_window, text="Quantité du produit:", font=("Consolas", 14))
        label_quantity.pack(pady=5)
        entry_quantity = Entry(add_window, font=("Consolas", 14))
        entry_quantity.pack(pady=5)

        label_category = Label(add_window, text="Catégorie du produit:", font=("Consolas", 14))
        label_category.pack(pady=5)

        category_combobox_add = ttk.Combobox(add_window, values=category_names, font=("Consolas", 14))
        category_combobox_add.pack(pady=5)

        def submit_produit():
            # Récupérer les informations et ajouter le produit à la base de données
            name = entry_name.get()
            description = entry_desc.get()
            price = entry_price.get()
            quantity = entry_quantity.get()
            category_name = category_combobox_add.get()
            category_id = next((cat[1] for cat in categories if cat[0] == category_name), None)
            store.ajouter_produit(name, description, price, quantity, category_id)
            add_window.destroy()  # Fermer la fenêtre d'ajout

        bouton_add = Button(add_window, text="Ajouter", command=submit_produit, font=("Consolas", 14))
        bouton_add.pack(pady=20)

    bouton_ajouter = Button(frame_buttons, text="Ajouter un produit", command=ajouter_produit_window, font=("Courier", 18))
    bouton_ajouter.pack(pady=10)

    # Suppression d'un produit
    def supprimer_produit_window():
        """Fonction pour supprimer un produit"""
        delete_window = Toplevel(window)
        delete_window.title("Supprimer un produit")
        delete_window.geometry("400x400")

        label_product_id = Label(delete_window, text="ID du produit à supprimer:", font=("Consolas", 14))
        label_product_id.pack(pady=5)
        entry_product_id = Entry(delete_window, font=("Consolas", 14))
        entry_product_id.pack(pady=5)

        def submit_delete():
            product_id = entry_product_id.get()
            store.supprimer_produit(product_id)
            delete_window.destroy()  # Fermer la fenêtre de suppression

        bouton_delete = Button(delete_window, text="Supprimer", command=submit_delete, font=("Consolas", 14))
        bouton_delete.pack(pady=20)

    bouton_supprimer = Button(frame_buttons, text="Supprimer un produit", command=supprimer_produit_window, font=("Courier", 18))
    bouton_supprimer.pack(pady=10)

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
