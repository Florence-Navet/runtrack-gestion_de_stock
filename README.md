# Gestion de Stock - Magasin (MangaStore)

![preview main](main.jpg)

## Description du projet

Ce projet permet la gestion de stock d'un magasin en Python en utilisant une base de données MySQL. L'application permet de gérer les produits et les catégories d'un magasin, avec une interface graphique simple pour interagir avec les produits en stock.

## Fonctionnalités

- **Affichage des produits** : La liste complète des produits en stock est affichée dans une interface graphique.
- **Ajout de produit** : L'utilisateur peut ajouter de nouveaux produits avec des informations comme le nom, la description, le prix, la quantité et la catégorie.
- **Modification de produit** : L'utilisateur peut modifier les détails d'un produit existant (stock, prix...).
- **Suppression de produit** : L'utilisateur peut supprimer des produits de la base de données.
- **Filtrage par catégorie** : Il est possible de filtrer les produits en fonction de la catégorie.
- **Exportation CSV** : Les produits peuvent être exportés au format CSV pour une gestion externe.
- **Interface graphique** : L'interface graphique est réalisée avec Tkinter et affiche les produits sous forme de tableau avec des options pour ajouter, supprimer et modifier les produits.

## Structure de la base de données

### Base de données : `mangastore`

1. **Table `category`** :

   - `id` : clé primaire, entier, auto-incrément
   - `name` : nom de la catégorie, varchar(255)

2. **Table `product`** :
   - `id` : clé primaire, entier, auto-incrément
   - `name` : nom du produit, varchar(255)
   - `description` : description du produit, texte
   - `price` : prix du produit, entier
   - `quantity` : quantité en stock, entier
   - `id_category` : clé étrangère qui référence `category.id`

### Exemple de création de base de données et insertion :

```sql
CREATE DATABASE IF NOT EXISTS mangastore;
USE mangastore;

CREATE TABLE IF NOT EXISTS category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    id_category INT,
    FOREIGN KEY (id_category) REFERENCES category(id) ON DELETE CASCADE
);

INSERT INTO category (name) VALUES ('Manga Shonen'), ('Manga Shojo'), ('Manga Seinen'), ('Goodies'), ('Figurines');


```

---

# Installation

**Prérequis**

- **Python 3.x** : Assurez-vous que Python est installé sur votre machine.
- **MySQL** : Vous devez avoir une instance MySQL en cours d'exécution et créer la base de données `mangastore`.
- **Bibliothèques Python** : + **mysql-connector-python** : Pour la connexion à MySQL. + **tkinter** : Pour l'interface graphique.

**Installation des dépendances**
Vous pouvez installer les bibliothèques nécessaires via pip :

```bash
pip install mysql-connector-python
pip install pandas
```

# Utilisation

**Lancer le programme**

1. Clonez ou téléchargez ce projet sur votre machine locale.
2. Assurez-vous que MySQL est correctement configuré et que la base de données `mangastore` est créée avec les bonnes tables.
3. Exécutez le programme en lançant le fichier Python principal :

```bash
python mangastore.py
```

**Fonctionalités de l'inferface graphique**

- **Affichage des produits** : La liste des produits s'affiche dans un tableau.
- **Ajout d'un produit** : Cliquez sur le bouton "Ajouter un produit" pour ouvrir un formulaire d'ajout.

# Auteurs

- **Florence Navet**
- **Projet open-source**

# Licence

Ce projet est sous la licence MIT - voir le fichier LICENSE pour plus de détails.

`Ce README contient les informations essentielles pour expliquer ton projet. Tu peux le modifier selon tes besoins, ajouter des détails sur l'interface graphique ou des fonctionnalités supplémentaires.`
