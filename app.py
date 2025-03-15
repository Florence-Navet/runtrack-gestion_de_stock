from tkinter import *
import tkinter.ttk as ttk  # Importer ttk pour utiliser Combobox
from mangaStore import MangaStore
import csv
from tkinter import filedialog


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

    frame_bottom_buttons = Frame(frame_boutique, bg='#ab7e9c')
    frame_bottom_buttons.pack(side=BOTTOM, fill=X, pady=10)  

    # Créer un frame pour l'image et les boutons dans la boutique
    frame_image_button = Frame(frame_boutique, bg='#ab7e9c')
    frame_image_button.pack(expand=YES, fill=BOTH)

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
    treeview.column('ID', width=80)          # Colonne ID 
    treeview.column('Nom', width=200)        # Colonne Nom
    treeview.column('Description', width=300)# Colonne Description
    treeview.column('Prix', width=100)       # Colonne Prix 
    treeview.column('Stock', width=100)      # Colonne Stock 
    treeview.column('Catégorie', width=150)  # Colonne Catégorie 

    # Dimensionner hauteur lignes (en ajustant la police et le padding)
    style = ttk.Style()
    style.configure("Treeview",
                    font=("Arial", 12),  
                    rowheight=30)  # Ajuster la hauteur des lignes (en pixels)

    # Appliquer le style au Treeview
    treeview.configure(style="Treeview")

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

    # Créer un frame pour les boutons
    frame_buttons = Frame(frame_image_button, bg='#ab7e9c')
    frame_buttons.pack(side=TOP, pady=30)  # Une seule déclaration de frame_buttons

    # Créer un Combobox pour la sélection de la catégorie
    label_category = Label(frame_buttons, text="", font=("Consolas", 20), bg='#ab7e9c')
    label_category.grid(row=0, column=2, padx=10, pady=10, columnspan=3, sticky='e')

    category_combobox = ttk.Combobox(frame_buttons, values=category_names, font=("Consolas", 12))
    category_combobox.grid(row=1, column=1, padx=10, pady=10, columnspan=2, sticky='n')
    category_combobox.set("catégorie")

    # Bouton pour appliquer le filtre
    bouton_filtrer = Button(frame_buttons, text="Appliquer Filtre", command=appliquer_filtre, font=("Courier", 12))
    bouton_filtrer.grid(row=1, column=3, padx=10, pady=10, columnspan=3, sticky='n')

    # Créer un bouton pour afficher tous les produits
    bouton_afficher_tous = Button(frame_buttons, text="Afficher produits", command=lambda: afficher_produits_boutique(), font=("Courier", 12))
    bouton_afficher_tous.grid(row=1, column=0, padx=10, pady=10, columnspan=1, sticky="n")

    def exporter_csv():
            # Créer une instance de MangaStore
            store = MangaStore()

            # Récupérer tous les produits de la boutique
            produits = store.afficher_produits()
            
            # Ouvrir une boîte de dialogue pour sélectionner où sauvegarder le fichier CSV
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            
            if file_path:
                # Créer le fichier CSV
                with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    # Écrire les en-têtes du CSV
                    writer.writerow(['ID', 'Nom', 'Description', 'Prix', 'Stock', 'Catégorie'])
                    # Ajouter les produits au fichier CSV
                    for produit in produits:
                        writer.writerow([produit[0], produit[1], produit[2], f"{produit[3]}€", produit[4], produit[5]])

                print(f"Les produits ont été exportés vers {file_path}")
            else:
                print("Exportation annulée.")
    bouton_export_csv = Button(frame_buttons, text="Exporter CSV", command=exporter_csv, font=("Courier", 12))
    bouton_export_csv.grid(row=0, column=4, padx=10, pady=10, columnspan=2, sticky='n')

    # Ajout d'un produit
    def ajouter_produit_window():
        """Fonction pour ajouter un produit"""
        add_window = Toplevel(window)
        add_window.title("Ajouter un produit")
        add_window.geometry("500x600")

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

        def recup_produit():
            # Récupérer les informations et ajouter le produit à la base de données
            name = entry_name.get()
            description = entry_desc.get()
            price = entry_price.get()
            quantity = entry_quantity.get()
            category_name = category_combobox_add.get()
            category_id = next((cat[1] for cat in categories if cat[0] == category_name), None)
            store.ajouter_produit(name, description, price, quantity, category_id)
            add_window.destroy()  # Fermer la fenêtre d'ajout
            afficher_produits_boutique(category_name)

        bouton_add = Button(add_window, text="Ajouter", command=recup_produit, font=("Consolas", 14))
        bouton_add.pack(pady=20)

    bouton_ajouter = Button(frame_buttons, text="Ajouter produit", command=ajouter_produit_window, font=("Courier", 12))
    bouton_ajouter.grid(row=0, column=0, padx=10, pady=10)


    # Suppression d'un produit
    def supprimer_produit_window():
        """Fenêtre pour supprimer un produit."""
        delete_window = Toplevel(window)
        delete_window.title("Supprimer un produit")
        delete_window.geometry("500x600")

        # Sélectionner la catégorie
        label_category = Label(delete_window, text="Sélectionner la catégorie:", font=("Consolas", 14))
        label_category.pack(pady=5)
        
        category_combobox = ttk.Combobox(delete_window, values=category_names, font=("Consolas", 14))
        category_combobox.pack(pady=5)

        # Sélectionner le produit à supprimer
        label_product = Label(delete_window, text="Sélectionner le produit à supprimer:", font=("Consolas", 14))
        label_product.pack(pady=5)

        product_combobox = ttk.Combobox(delete_window, font=("Consolas", 14))
        product_combobox.pack(pady=5)

        # Fonction pour mettre à jour la liste des produits en fonction de la catégorie choisie
        def mise_a_jour_liste_produits(event=None):
            selected_category = category_combobox.get()
            # Vérifier si une catégorie est sélectionnée
            if selected_category:
                filtered_products = store.filtrer_produits_par_categorie(selected_category)
                product_combobox['values'] = [p[1] for p in filtered_products]  # Remplir le combobox avec les noms des produits
                product_combobox.set('')  # Réinitialiser la sélection du produit
            else:
                product_combobox['values'] = []
                product_combobox.set('')

        category_combobox.bind("<<ComboboxSelected>>", mise_a_jour_liste_produits)

        # Fonction pour supprimer le produit sélectionné
        def envoi_suppression():
            selected_category = category_combobox.get()
            selected_product_name = product_combobox.get()

            # Vérification des sélections
            if not selected_category or not selected_product_name:
                label_info.config(text="Veuillez sélectionner un produit", fg="red")
                return

            # Récupérer l'ID de la catégorie sélectionnée
            category_id = next((cat[1] for cat in categories if cat[0] == selected_category), None)
            
            # Vérification si l'ID de catégorie est valide
            if not category_id:
                label_info.config(text="Catégorie invalide", fg="red")
                return
            
            # Filtrer les produits de la catégorie sélectionnée
            filtered_products = store.filtrer_produits_par_categorie(selected_category)
            
            # Trouver le produit en fonction de son nom
            product = next((p for p in filtered_products if p[1] == selected_product_name), None)
            
            if product:
                product_id = product[0]  # L'ID du produit est le premier élément du tuple
                print(f"Suppression du produit : {selected_product_name}, ID : {product_id}")  # Débogage

                # Appel à la méthode de suppression
                store.supprimer_produit(product_id)
                
                # Mise à jour du message de succès
                label_info.config(text="Produit supprimé avec succès", fg="green")
                delete_window.after(1000, delete_window.destroy)  # Fermer après 1 seconde
                afficher_produits_boutique()
            else:
                label_info.config(text="Produit introuvable", fg="red")

        # Bouton de suppression
        bouton_delete = Button(delete_window, text="Supprimer", command=envoi_suppression, font=("Consolas", 14))
        bouton_delete.pack(pady=20)

        # Label pour les messages d'erreur/succès
        label_info = Label(delete_window, text="", font=("Consolas", 12))
        label_info.pack(pady=5)

    # Bouton pour ouvrir la fenêtre de suppression
    bouton_supprimer = Button(frame_buttons, text="Supprimer produit", command=supprimer_produit_window, font=("Courier", 12))
    bouton_supprimer.grid(row=0, column=1, padx=10, pady=10)





    def modifier_produit_window():
        """Fonction pour modifier un produit"""
        modify_window = Toplevel(window)
        modify_window.title("Modifier un produit")
        modify_window.geometry("500x600")

        # Sélectionner la catégorie actuelle
        label_current_category = Label(modify_window, text="Sélectionner la catégorie actuelle:", font=("Consolas", 14))
        label_current_category.pack(pady=5)
        
        category_combobox_current = ttk.Combobox(modify_window, values=category_names, font=("Consolas", 14))
        category_combobox_current.pack(pady=5)

        # Sélectionner le produit à modifier dans la catégorie
        label_current_name = Label(modify_window, text="Sélectionner le produit à modifier:", font=("Consolas", 14))
        label_current_name.pack(pady=5)

        product_combobox = ttk.Combobox(modify_window, font=("Consolas", 14))
        product_combobox.pack(pady=5)


        def mise_a_jour_liste_produit(event=None):
            # Récupérer la catégorie actuelle
            selected_category = category_combobox_current.get()
            print(f"Catégorie sélectionnée : {selected_category}")  # Affichage de la catégorie sélectionnée

            # Filtrer les produits selon la catégorie choisie
            filtered_products = store.filtrer_produits_par_categorie(selected_category)
            
            # Affichage des produits filtrés dans le terminal
            print("Produits filtrés :")
            for product in filtered_products:
                print(product)  # Afficher chaque produit (id, nom, description, prix, quantité, catégorie)
            
            # Mettre à jour les produits dans le combobox
            product_combobox['values'] = [p[1] for p in filtered_products]  # Affiche les noms des produits
            product_combobox.set('')  # Réinitialiser la sélection du produit

        # Lier la mise à jour de la liste des produits à la sélection de la catégorie
        category_combobox_current.bind("<<ComboboxSelected>>", mise_a_jour_liste_produit)

        # Sélectionner la nouvelle catégorie
        label_new_category = Label(modify_window, text="Sélectionner la nouvelle catégorie:", font=("Consolas", 14))
        label_new_category.pack(pady=5)

        category_combobox_new = ttk.Combobox(modify_window, values=category_names, font=("Consolas", 14))
        category_combobox_new.pack(pady=5)

        # Nouveau prix
        label_price = Label(modify_window, text="Prix du produit:", font=("Consolas", 14))
        label_price.pack(pady=5)
        entry_price = Entry(modify_window, font=("Consolas", 14))
        entry_price.pack(pady=5)


        def envoi_modification():
            current_category_name = category_combobox_current.get()
            current_product_name = product_combobox.get()
            new_category_name = category_combobox_new.get()
            new_price = entry_price.get()  # Récupération du nouveau prix

            # Trouver les IDs des catégories
            current_category_id = next((cat[1] for cat in categories if cat[0] == current_category_name), None)
            new_category_id = next((cat[1] for cat in categories if cat[0] == new_category_name), None)

            # Vérification si les catégories sont valides
            if current_category_id is None or new_category_id is None:
                print("Erreur : Catégorie invalide.")
                return

            # Trouver le produit à partir de son nom dans la catégorie sélectionnée
            current_product = next((p for p in store.filtrer_produits_par_categorie(current_category_name) if p[1] == current_product_name), None)

            # Ajout d'un affichage pour déboguer
            print(f"Produit sélectionné : {current_product}")  # Afficher le produit sélectionné

            if current_product:
                product_id = current_product[0]

                # Vérification et conversion du prix
                try:
                    new_price = float(new_price) if new_price else current_product[3]
                except ValueError:
                    print("Erreur : Le prix doit être un nombre valide.")
                    return

                # Modifier le produit
                store.modifier_produit(product_id, current_product_name, current_product[2], new_price, current_product[4], new_category_id)
                modify_window.destroy()  # Fermer la fenêtre après modification
                afficher_produits_boutique()
            else:
                print("Produit introuvable")


        # Ajouter un bouton pour valider la modification
        bouton_validate = Button(modify_window, text="Valider", command=envoi_modification, font=("Consolas", 14))
        bouton_validate.pack(pady=20)




    # Ajouter un bouton pour modifier le produit dans la fenêtre des boutons
    def ajouter_bouton_modifier():
        bouton_modifier = Button(frame_buttons, text="Modifier produit", command=modifier_produit_window, font=("Courier", 12))
        bouton_modifier.grid(row=0, column=3, padx=10, pady=10)  # Positionnez-le là où vous le souhaitez

    # Appeler cette fonction pour ajouter le bouton "Modifier produit" au frame
    ajouter_bouton_modifier()


# Ajouter un bouton pour revenir à la fenêtre principale
    def revenir_main_window():
            frame_boutique.pack_forget()  # Masquer la fenêtre boutique
            frame_main.pack(expand=YES)   # Afficher la fenêtre principale

        # Ajouter un bouton "Retour" dans le frame en bas
    bouton_retour = Button(frame_bottom_buttons, text="Retour", command=revenir_main_window, font=("Courier", 18))
    bouton_retour.pack(pady=10)  # Le bouton retour sera maintenant en bas du frame
    # Afficher la boutique
    frame_boutique.pack(expand=YES, fill=BOTH)

# Fenêtre principale: Ajouter un bouton
fenetre_button = Button(frame_main, text="Découvrir boutique", font=("Courier", 18), bg='#FFFFFF', fg='#ab7e9c', command=ouvrir_boutique)
fenetre_button.pack(side=TOP, pady=10, fill=X)

# Fenêtre principale: Ajouter la frame dans la fenêtre
frame_main.pack(expand=YES)

# Afficher la fenêtre principale
window.mainloop()
