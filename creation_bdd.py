import sqlite3

#ouverture et initialisation de la base de données
db_persos=sqlite3.connect('personnages3.sqlite')
db_persos.text_factory = lambda x: str(x,'utf8')
cur = db_persos.cursor()


#creation de la table Personnages
cur.execute("""CREATE TABLE Personnages(
id INTEGER PRIMARY KEY AUTOINCREMENT,
genre TEXT ,
sexe TEXT,
age INT,
origine TEXT,
religion TEXT,
classe TEXT,
caractere1 TEXT,
caractere2 TEXT);""")
db_persos.commit()

#creation de la table Livres
cur.execute("""CREATE TABLE Livres(
id INTEGER PRIMARY KEY AUTOINCREMENT,
titre TEXT ,
nom_principal TEXT,
nb_chapitres INT,
theme TEXT,
epoque TEXT);""")
db_persos.commit()

#creation de la table pont
cur.execute("""CREATE TABLE Roles(
id_livre INT,
id_perso INT,
nom TEXT,
fonction TEXT);""")
db_persos.commit()


cur.execute("""INSERT INTO Personnages (genre, sexe, age, origine, religion, classe, caractere1, caractere2) VALUES
( 'femme', 'asexuel', 40, 'Sud-Est', 'oasisme', 'tres pauvre', 'intelligente', 'humble'),
( 'non-binaire', 'homosexuel', 0, 'centre', 'duologisme', 'petite bourgeoisie', 'determine', 'colerique'),
( 'homme', 'heterosexuel', 60, 'ravageur', 'oasisme', 'modeste', 'reac', 'de confiance');""")
db_persos.commit()

cur.execute("""INSERT INTO Livres (titre, nom_principal, nb_chapitres, theme, epoque) VALUES
( "analyse d'une perle", 'Rhea', 30, 'anéantissement des elfes', 'entre 950 et 1012'),
( "analyse d'un couteau", 'Pablo', 30, 'révolte des ravageurs', 'entre 50 et 80'),
( "analyse d'un medaillon", 'Lydia', 30, "vie d'une criminelle", 'vers 4000');""")
db_persos.commit()

cur.execute("""INSERT INTO Roles (id_livre, id_perso, nom, fonction) VALUES
(2, 3, 'Basil', 'tavernier');""")
db_persos.commit()


db_persos.close()
