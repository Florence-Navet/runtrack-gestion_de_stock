import mysql.connector

class MangaStore:
    """
    Classe pour gérer un magasin de mangas avec une base de données MySQL.
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
            produit = self.cursor.fetchone()
            
            if not produit:
                print(f"Erreur : Aucun produit trouvé avec l'ID {product_id}.")
                return

            self.cursor.execute("DELETE FROM product WHERE id = %s", (product_id,))
            self.db.commit()

            print(f"Produit avec l'ID {product_id} supprimé avec succès !")
        except mysql.connector.Error as err:
            print(f"Erreur MySQL : {err}")

    def afficher_produits(self):
        """Affiche tous les produits du stock."""
        self.cursor.execute("""
            SELECT product.id, product.name, product.description, product.price, product.quantity, category.name
            FROM product
            JOIN category ON product.id_category = category.id
        """)
        produits = self.cursor.fetchall()

        if not produits:
            print("\nAucun produit trouvé dans la base de données.")
            return []

        for p in produits:
            print(f"ID: {p[0]}, Nom: {p[1]}, Description: {p[2]}, Prix: {p[3]}€, Stock: {p[4]}, Catégorie: {p[5]}")
        return produits

    def fermer_connexion(self):
        """Ferme la connexion à la base de données."""
        self.cursor.close()
        self.db.close()
        print("Connexion MySQL fermée.")

# --- Interface CLI ---
def menu():
    store = MangaStore()
    while True:
        print("\n MENU PRINCIPAL")
        print("1. Afficher les produits")
        print("2. Ajouter un produit")
        print("3. Quitter")
        choix = input("Choisissez une option : ")

        match choix:
            case "1":
                store.afficher_produits()
            case "2":
                name = input("Nom du produit : ")
                description = input("Description : ")
                price = float(input("Prix (€) : "))
                quantity = int(input("Stock : "))
                category_id = int(input("ID de la catégorie : "))
                store.ajouter_produit(name, description, price, quantity, category_id)
            case "3":
                store.fermer_connexion()
                break
            case _:
                print("Option invalide, réessayez.")

if __name__ == "__main__":
    menu()
