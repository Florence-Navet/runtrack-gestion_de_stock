import mysql.connector
import csv

class MangaStore:
    """
    TODO:
    - Calcul du stock total : Calculer la valeur totale du stock en fonction des prix et des quantités.
    - Affichage des produits les plus populaires(optionnel) : Trier les produits par leur quantité en stock.
    - Gestion des commandes (optionnel) : Suivi des produits commandés par les clients.
    - Gestion des utilisateurs (optionnel) : Système de gestion des utilisateurs (administrateurs, clients).
    - Recherche par nom de produit : Permettre à l'utilisateur de rechercher un produit par son nom.

    """

    def __init__(self):
        """Connexion à la base de données MySQL."""
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456",  
                database="mangastore"
            )
            self.cursor = self.db.cursor()
            print("Connexion réussie à MySQL !")
        
        except mysql.connector.Error as err:
            print(f"Erreur de connexion : {err}")
            exit()

        self.create_database_and_tables()

    def create_database_and_tables(self):
        """Création de la base de données et des tables si elles n'existent pas."""
        try:
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS mangastore")
            self.db.database = "mangastore"

            self.cursor.execute(""" 
                CREATE TABLE IF NOT EXISTS category (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL
                )
            """)

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

            categories = ["Manga Shonen", "Manga Shojo", "Manga Seinen", "Goodies", "Figurines"]
            for category in categories:
                self.cursor.execute("SELECT COUNT(*) FROM category WHERE name = %s", (category,))
                if self.cursor.fetchone()[0] == 0:
                    self.cursor.execute("INSERT INTO category (name) VALUES (%s)", (category,))

            self.db.commit()
        except mysql.connector.Error as err:
            print(f"Erreur lors de la création de la base de données ou des tables : {err}")

    def filtrer_produits_par_categorie(self, category_name):
        """Filtre les produits par catégorie."""
        try:
            self.cursor.execute("""
                SELECT p.id, p.name, p.description, p.price, p.quantity, c.name
                FROM product p 
                LEFT JOIN category c ON p.id_category = c.id
                WHERE c.name = %s
            """, (category_name,))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Erreur MySQL : {err}")
            return []

    def ajouter_produit(self, name, description, price, quantity, category_id):
        """Ajoute un produit avec validation et debug."""
        try:
            self.cursor.execute("SELECT * FROM category WHERE id = %s", (category_id,))
            category = self.cursor.fetchone()
            if not category:
                print(f"Erreur : La catégorie ID {category_id} n'existe pas.")
                return

            query = "INSERT INTO product (name, description, price, quantity, id_category) VALUES (%s, %s, %s, %s, %s)"
            values = (name, description, price, quantity, category_id)
            self.cursor.execute(query, values)
            self.db.commit()

            print(f"Produit '{name}' ajouté avec succès !")
        except mysql.connector.Error as err:
            print(f"Erreur MySQL : {err}")

    def supprimer_produit(self, product_id):
        """Supprime un produit de la base de données en fonction de son ID."""
        try:
            self.cursor.execute("SELECT * FROM product WHERE id = %s", (product_id,))
            if not self.cursor.fetchone():
                print(f"Erreur : Produit avec ID {product_id} non trouvé.")
                return

            self.cursor.execute("DELETE FROM product WHERE id = %s", (product_id,))
            self.db.commit()
            print(f"Produit avec ID {product_id} supprimé.")
        except mysql.connector.Error as err:
            print(f"Erreur MySQL : {err}")

    def afficher_produits(self):
        """Affiche tous les produits dans la base de données."""
        try:
            self.cursor.execute("""SELECT p.id, p.name, p.description, p.price, p.quantity, c.name
                                   FROM product p 
                                   LEFT JOIN category c ON p.id_category = c.id""")
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Erreur MySQL : {err}")
            return []
        
    def get_liste_noms_produits(self):
        """Récupère la liste des noms des produits depuis la base de données"""
        self.cursor.execute("SELECT nom FROM produits")  # Ajuste la table et la colonne selon ton schéma
        result = self.cursor.fetchall()
        return [row[0] for row in result]  # Retourne une liste contenant uniquement les noms


    def fermer_connexion(self):
        """Ferme la connexion à la base de données."""
        self.cursor.close()
        self.db.close()
        print("Connexion MySQL fermée.")

    def modifier_produit(self, product_id, name, description, price, quantity, category_id):
        """Modifie un produit existant dans la base de données."""
        try:
            # Vérifier si le produit existe
            self.cursor.execute("SELECT * FROM product WHERE id = %s", (product_id,))
            if not self.cursor.fetchone():
                print(f"Erreur : Produit avec ID {product_id} non trouvé.")
                return

            # Mettre à jour les informations du produit
            query = """UPDATE product
                       SET name = %s, description = %s, price = %s, quantity = %s, id_category = %s
                       WHERE id = %s"""
            values = (name, description, price, quantity, category_id, product_id)
            self.cursor.execute(query, values)
            self.db.commit()

            print(f"Produit avec ID {product_id} modifié avec succès !")
        except mysql.connector.Error as err:
            print(f"Erreur MySQL : {err}")

    def exporter_en_csv(self):
        """Exporte les produits en fichier CSV."""
        try:
            produits = self.afficher_produits()
            if produits:
                with open('produits.csv', 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(["ID", "Nom", "Description", "Prix (€)", "Stock", "Catégorie"])
                    for p in produits:
                        writer.writerow([p[0], p[1], p[2], p[3], p[4], p[5]])
                print("Les produits ont été exportés avec succès dans 'produits.csv'.")
            else:
                print("Aucun produit à exporter.")
        except Exception as e:
            print(f"Erreur lors de l'exportation : {e}")

    def calculer_stock_total(self):
        """Calculer la valeur totale du stock."""
        try:
            self.cursor.execute("SELECT price, quantity FROM product")
            produits = self.cursor.fetchall()
            total = sum(p[0] * p[1] for p in produits)
            print(f"Valeur totale du stock : {total}€")
        except mysql.connector.Error as err:
            print(f"Erreur MySQL : {err}")


# --- Menu terminal---
def menu():
    store = MangaStore()
    while True:
        print("\n MENU PRINCIPAL")
        print("1. Afficher les produits")
        print("2. Ajouter un produit")
        print("3. Supprimer un produit")
        print("4. Filtrer les produits par catégorie")
        print("5. Modifier un produit")
        print("6. Exporter en CSV")
        print("7. Calculer le stock total")
        print("8. Quitter")
        choix = input("Choisissez une option : ")

        match choix:
            case "1":
                produits = store.afficher_produits()
                if produits:
                    for p in produits:
                        print(f"ID: {p[0]}, Nom: {p[1]}, Description: {p[2]}, Prix: {p[3]}€, Stock: {p[4]}, Catégorie: {p[5]}")
            case "2":
                name = input("Nom du produit : ")
                description = input("Description : ")
                price = float(input("Prix (€) : "))
                quantity = int(input("Stock : "))
                category_id = int(input("ID de la catégorie : "))
                store.ajouter_produit(name, description, price, quantity, category_id)
            case "3":
                product_id = int(input("Entrez l'ID du produit à supprimer : "))
                store.supprimer_produit(product_id)
            case "4":
                category_name = input("Nom de la catégorie à filtrer : ")
                produits = store.filtrer_produits_par_categorie(category_name)
                if produits:
                    for p in produits:
                        print(f"ID: {p[0]}, Nom: {p[1]}, Description: {p[2]}, Prix: {p[3]}€, Stock: {p[4]}, Catégorie: {p[5]}")
                else:
                    print(f"Aucun produit trouvé dans la catégorie '{category_name}'.")
            case "5":
                product_id = int(input("Entrez l'ID du produit à modifier : "))
                name = input("Nouveau nom du produit : ")
                description = input("Nouvelle description : ")
                price = float(input("Nouveau prix (€) : "))
                quantity = int(input("Nouveau stock : "))
                category_id = int(input("Nouvel ID de la catégorie : "))
                store.modifier_produit(product_id, name, description, price, quantity, category_id)
            case "6":
                store.exporter_en_csv()
            case "7":
                store.calculer_stock_total()
            case "8":
                store.fermer_connexion()
                break
            case _:
                print("Option invalide, réessayez.")

if __name__ == "__main__":
    menu()
