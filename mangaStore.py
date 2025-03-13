import mysql.connector

class MangaStore:
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

            # Vérifier la base de données en cours
            self.cursor.execute("SELECT DATABASE();")
            current_db = self.cursor.fetchone()
            print(f"Base de données actuelle : {current_db[0]}")

        except mysql.connector.Error as err:
            print(f"Erreur de connexion : {err}")
            exit()

        # Création des tables et des catégories
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

            # Vérification des catégories ajoutées
            self.cursor.execute("SELECT * FROM category")
            print("Catégories disponibles :", self.cursor.fetchall())

        except mysql.connector.Error as err:
            print(f"Erreur lors de la création de la base de données ou des tables : {err}")

    def ajouter_produit(self, name, description, price, quantity, category_id):
        """Ajoute un produit avec validation et debug."""
        try:
            # Vérifier si la catégorie existe
            self.cursor.execute("SELECT * FROM category WHERE id = %s", (category_id,))
            category = self.cursor.fetchone()
            if not category:
                print(f"Erreur : La catégorie ID {category_id} n'existe pas. Vérifiez avec SELECT * FROM category.")
                return

            query = "INSERT INTO product (name, description, price, quantity, id_category) VALUES (%s, %s, %s, %s, %s)"
            values = (name, description, price, quantity, category_id)

            print(f"🔹 Tentative d'insertion : {values}")
            self.cursor.execute(query, values)
            self.db.commit()

            print(f"Produit '{name}' ajouté avec succès !")
        
        except mysql.connector.Error as err:
            print(f"Erreur MySQL : {err}")

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

    def fermer_connexion(self):
        """Ferme la connexion à la base de données."""
        self.cursor.close()
        self.db.close()
        print("Connexion MySQL fermée.")

# --- Interface CLI ---
def menu():
    print("🛒 Ouverture du magasin !")
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
                print("Fermeture du programme...")
                store.fermer_connexion()
                break
            
            case _:
                print("Option invalide, réessayez.")

if __name__ == "__main__":
    menu()
