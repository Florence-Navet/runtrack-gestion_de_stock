import mysql.connector

class MangaStore:
    def __init__(self):
        """Connexion à la base de données MySQL."""
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456",  # Remplace par ton mot de passe
                database="store"
            )
            self.cursor = self.db.cursor()
            print("Connexion réussie à MySQL !")

            # Vérifier la base de données en cours
            self.cursor.execute("SELECT DATABASE();")
            current_db = self.cursor.fetchone()
            print(f"Base de données actuelle : {current_db[0]}")

        except mysql.connector.Error as err:
            print(f"Erreur de connexion : {err}")
            exit()

        # Création de la base de données et des tables si elles n'existent pas
        self.create_database_and_tables()

    def create_database_and_tables(self):
        """Création de la base de données et des tables si elles n'existent pas"""
        try:
            # Création de la base de données
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS store")
            self.db.database = "store"  # Connexion à la base de données 'store'

            # Création de la table 'category'
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS category (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL
                )
            """)

            # Création de la table 'product'
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS product (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    price DECIMAL(10, 2) NOT NULL,
                    quantity INT NOT NULL,
                    id_category INT,
                    FOREIGN KEY (id_category) REFERENCES category(id) ON DELETE CASCADE
                )
            """)

            # Insertion de catégories seulement si elles n'existent pas déjà
            categories = ["Manga Shonen", "Manga Shojo", "Manga Seinen", "Goodies", "Figurines"]
            for category in categories:
                self.cursor.execute("SELECT COUNT(*) FROM category WHERE name = %s", (category,))
                if self.cursor.fetchone()[0] == 0:  # Si la catégorie n'existe pas déjà
                    self.cursor.execute("INSERT INTO category (name) VALUES (%s)", (category,))
            
            self.db.commit()

            # Insertion de produits si la table est vide
            self.cursor.execute("SELECT COUNT(*) FROM product")
            if self.cursor.fetchone()[0] == 0:
                self.cursor.executemany("""
                    INSERT INTO product (name, description, price, quantity, id_category)
                    VALUES (%s, %s, %s, %s, %s)
                """, [
                    ("One Piece - Tome 1", "Le premier tome des aventures de Luffy.", 8, 50, 1),
                    ("Dragon Ball Z - Tome 3", "Goku contre Vegeta !", 9, 30, 1),
                    ("Demon Slayer - Tome 5", "Tanjiro affronte de nouveaux ennemis.", 10, 40, 1),
                    ("Sailor Moon - Tome 2", "Les aventures de Sailor Moon.", 8, 20, 2),
                    ("Attaque des Titans - Tome 10", "Eren découvre la vérité.", 11, 15, 3),
                    ("Figurine Luffy", "Superbe figurine de Luffy en Gear 5.", 25, 10, 5)
                ])
                print("Produits insérés dans la base de données.")
            
            self.db.commit()

        except mysql.connector.Error as err:
            print(f"Erreur lors de la création de la base de données ou des tables : {err}")


    def afficher_produits(self):
        """Affiche tous les produits du stock."""
        print("\nExécution de la requête pour afficher les produits...")
        self.cursor.execute("""
            SELECT product.id, product.name, product.description, product.price, product.quantity, category.name 
            FROM product 
            JOIN category ON product.id_category = category.id
        """)
        produits = self.cursor.fetchall()

        if not produits:
            print("\nAucun produit trouvé dans la base de données.")
            return

        print("\nListe des Produits :")
        for p in produits:
            print(f"ID: {p[0]}, Nom: {p[1]}, Description: {p[2]}, Prix: {p[3]}€, Stock: {p[4]}, Catégorie: {p[5]}")

    def ajouter_produit(self, name, description, price, quantity, category_id):
        """Ajoute un nouveau produit."""
        try:
            query = "INSERT INTO product (name, description, price, quantity, id_category) VALUES (%s, %s, %s, %s, %s)"
            values = (name, description, price, quantity, category_id)
            self.cursor.execute(query, values)
            self.db.commit()
            print(f"Produit '{name}' ajouté avec succès !")
        except mysql.connector.Error as err:
            print(f"Erreur lors de l'ajout du produit : {err}")

    def modifier_produit(self, product_id, price=None, quantity=None):
        """Modifie le prix ou la quantité d'un produit."""
        if price is not None:
            self.cursor.execute("UPDATE product SET price = %s WHERE id = %s", (price, product_id))
        if quantity is not None:
            self.cursor.execute("UPDATE product SET quantity = %s WHERE id = %s", (quantity, product_id))
        self.db.commit()
        print(f"Produit ID {product_id} mis à jour.")

    def supprimer_produit(self, product_id):
        """Supprime un produit par son ID."""
        self.cursor.execute("DELETE FROM product WHERE id = %s", (product_id,))
        self.db.commit()
        print(f"Produit ID {product_id} supprimé.")

    def filtrer_par_categorie(self, category_id):
        """Affiche les produits d’une catégorie donnée."""
        self.cursor.execute("SELECT id, name, description, price, quantity FROM product WHERE id_category = %s", (category_id,))
        produits = self.cursor.fetchall()
        print(f"\nProduits de la Catégorie {category_id}")
        for p in produits:
            print(f"ID: {p[0]}, Nom: {p[1]}, Prix: {p[3]}€, Stock: {p[4]}")

    def fermer_connexion(self):
        """Ferme la connexion à la base de données."""
        self.cursor.close()
        self.db.close()
        print("Connexion MySQL fermée.")

# --- Interface CLI ---
def menu():
    print("Ouverture du magasin !")  # Vérification
    store = MangaStore()

    while True:
        print("\nMENU PRINCIPAL")
        print("1. Afficher les produits")
        print("2. Ajouter un produit")
        print("3. Modifier un produit")
        print("4. Supprimer un produit")
        print("5. Filtrer les produits par catégorie")
        print("6. Quitter")
        choix = input("Choisissez une option : ")

        match choix:
            case "1":
                store.afficher_produits()
            case "2":
                name = input("Nom du produit : ")
                description = input("Description : ")
                price = int(input("Prix (€) : "))
                quantity = int(input("Stock : "))
                category_id = int(input("ID de la catégorie : "))
                store.ajouter_produit(name, description, price, quantity, category_id)
            case "3":
                product_id = int(input("ID du produit à modifier : "))
                price = input("Nouveau prix (laisser vide pour ne pas changer) : ")
                quantity = input("Nouvelle quantité (laisser vide pour ne pas changer) : ")
                store.modifier_produit(product_id, int(price) if price else None, int(quantity) if quantity else None)
            case "4":
                product_id = int(input("ID du produit à supprimer : "))
                store.supprimer_produit(product_id)
            case "5":
                category_id = int(input("ID de la catégorie à filtrer : "))
                store.filtrer_par_categorie(category_id)
            case "6":
                print("Fermeture du programme...")
                store.fermer_connexion()
                break
            case _:
                print("Option invalide, réessayez.")

if __name__ == "__main__":
    menu()
