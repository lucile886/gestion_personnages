from flask import Flask, render_template, request, redirect, url_for
import re
import sqlite3

monapp = Flask(__name__) #c'est bien un site interactif


@monapp.route("/")
def accueil():
    '''accueil du site'''
    return render_template("accueil.html")

@monapp.route("/ajout_personnage", methods=("GET", "POST"))
def ecriture_perso():
    '''inscription d'un nouveau personnage'''

    db_persos=sqlite3.connect('personnages3.sqlite')
    db_persos.row_factory = sqlite3.Row #pour l'avoir sous forme de dictionnaire
    cursor= db_persos.cursor()

    #on enregistre ses informations sur le serveur
    if request.method=='POST':
        genre = request.form['genre']
        sexe = request.form['sexe']
        age = request.form['age']
        origine = request.form['origine']
        religion = request.form['religion']
        classe = request.form['classe']
        caractereun = request.form['caractereun']
        caracteredeux = request.form['caracteredeux']
        enregistré = ("le personnage secondaire a bien été enregistré")

        #on ajoute le nouveau personnage à la table
        cursor.execute("""INSERT INTO Personnages (genre, sexe, age, origine, religion, classe, caractere1, caractere2) VALUES(?, ?, ?, ?, ?, ?, ?, ?);""", (genre, sexe, age, origine, religion, classe, caractereun, caracteredeux, ))
        db_persos.commit()
        db_persos.close()
        return render_template("ecriture_perso.html", message= enregistré )
    
    if "retourner à l'accueil" in request.form:
            return render_template("accueil.html")
    
    #s'il n'y a rien, on affiche la page pour l'inscrire  
    return render_template("ecriture_perso.html")

@monapp.route("/ajout_livre", methods=("GET", "POST"))
def ecriture_roman():
    '''inscription d'un nouveau livre'''

    db_persos=sqlite3.connect('personnages3.sqlite')
    db_persos.row_factory = sqlite3.Row #pour l'avoir sous forme de dictionnaire
    cursor= db_persos.cursor()

    #s'il a mis quelque chose, on enregistre ses informations sur le serveur
    if request.method=='POST':
        titre = request.form['titre']
        nom = request.form['nom']
        nb = request.form['nb']
        theme = request.form['theme']
        epoque = request.form['temps']
        enregistré = ("le roman a bien été enregistré")
        #si le bouton a été pressé on envoie à la page suivante
        if "retourner à l'accueil" in request.form:
            return render_template("accueil.html")
        #on ajoute le nouveau roman à la table
        cursor.execute("""INSERT INTO Livres (titre, nom_principal, nb_chapitres, theme, epoque) VALUES(?, ?, ?, ?, ?);""", (titre, nom, nb, theme, epoque, ))
        db_persos.commit()
        db_persos.close()
        return render_template("ecriture_roman.html", message= enregistré )
    #s'il n'y a rien, on affiche la page pour inscrire  
    return render_template("ecriture_roman.html")

@monapp.route("/recherche", methods=['GET'])
def recherche():
    '''page de recherche du site'''

    db_persos = sqlite3.connect('personnages3.sqlite')
    db_persos.row_factory = sqlite3.Row
    cursor = db_persos.cursor()

    # on regarde quelle barre de recherche a été remplie
    cherche_perso = request.args.get("recherche_perso")
    cherche_roman = request.args.get("recherche_roman")
    cherche_tous_perso = request.args.get("cherche_tous_perso")

    affichage_perso = None
    affichage_roman = None
    cherche_tous_perso = None
    message = None

    if cherche_perso:
        cherche_perso = cherche_perso.strip()
        cursor.execute("""
            SELECT * FROM Personnages 
            WHERE UPPER(genre) LIKE UPPER(?) 
               OR UPPER(sexe) LIKE UPPER(?) 
               OR UPPER(age) LIKE UPPER(?) 
               OR UPPER(origine) LIKE UPPER(?) 
               OR UPPER(religion) LIKE UPPER(?) 
               OR UPPER(classe) LIKE UPPER(?) 
               OR UPPER(caractere1) LIKE UPPER(?) 
               OR UPPER(caractere2) LIKE UPPER(?)
        """, ('%' + cherche_perso + '%',) * 8)
        affichage_perso = cursor.fetchall()

    if cherche_tous_perso:
        cherche_tous_perso = cherche_tous_perso.strip()
        cursor.execute("""
            SELECT * FROM Personnages;
        """)
        affichage_perso = cursor.fetchall()

    if cherche_roman:
        cherche_roman = cherche_roman.strip()
        cursor.execute("""
            SELECT * FROM Livres 
            WHERE UPPER(titre) LIKE UPPER(?) 
               OR UPPER(nom_principal) LIKE UPPER(?) 
               OR UPPER(theme) LIKE UPPER(?) 
               OR UPPER(epoque) LIKE UPPER(?)
        """, ('%' + cherche_roman + '%',) * 4)
        affichage_roman = cursor.fetchall()

    # Fermer la connexion à la fin
    db_persos.close()

    # Si aucun résultat
    if not affichage_perso and not affichage_roman and (cherche_perso or cherche_roman):
        message = "Aucun résultat trouvé."

    return render_template("recherche.html", 
                         affichage_perso=affichage_perso, 
                         affichage_roman=affichage_roman, 
                         message=message)
        
@monapp.route('/personnage/<int:id>')
def perso_details(id):

    db_persos=sqlite3.connect('personnages3.sqlite')
    db_persos.row_factory = sqlite3.Row #pour l'avoir sous forme de dictionnaire
    cursor= db_persos.cursor()
    
    # Se connecter à la base de données et récupérer les détails du personnage
    cursor.execute("""SELECT * FROM Personnages WHERE id = ?;""", (id,))
    perso = cursor.fetchone()  # Récupérer le personnage avec cet id
    cursor.execute("""SELECT Livres.titre, Livres.id FROM Livres JOIN Roles ON Livres.id = Roles.id_livre JOIN Personnages ON Roles.id_perso = Personnages.id WHERE Personnages.id = ?;""", (id,))
    livre = cursor.fetchone()
    cursor.execute("""SELECT nom FROM Roles WHERE Roles.id_perso = ?;""", (id,))
    nom = cursor.fetchone()
    db_persos.close()
    if perso and livre:
        return render_template("perso_detail.html", perso = perso, nom = nom, livre = livre)
    
    elif perso:
         return render_template("perso_detail.html", perso = perso)

@monapp.route('/roman/<int:id>')
def roman_details(id):

    db_persos=sqlite3.connect('personnages3.sqlite')
    db_persos.row_factory = sqlite3.Row #pour l'avoir sous forme de dictionnaire
    cursor= db_persos.cursor()
    
    # Se connecter à la base de données et récupérer les détails du livre
    cursor.execute("""SELECT * FROM Livres WHERE id = ?;""", (id,))
    roman = cursor.fetchone()  # Récupérer le livre avec cet id
    db_persos.close()
    if roman:
        return render_template("roman_detail.html", roman = roman)
    
    if "retourner à l'accueil" in request.form:
            return render_template("accueil.html")
    
    if "retourner à la recherche" in request.form:
            return render_template("recherche.html")
    
@monapp.route('/ajout', methods=['GET', 'POST'])
def ajout_perso_roman():
    message = None
    
    #on vérifie quel personnage est ajouté et où
    if request.method == 'POST':
        id_perso = request.form.get('id_perso')
        id_roman = request.form.get('id_roman')
        nom = request.form.get('nom')
        fonction = request.form.get('fonction')

        #si tous les champs sont remplis, on ajoute le personnage à la table
        if id_perso and id_roman and nom and fonction:
            try:
                id_perso = int(id_perso)
                id_roman = int(id_roman)

                db_persos = sqlite3.connect('personnages3.sqlite')
                db_persos.row_factory = sqlite3.Row
                cursor = db_persos.cursor()

                cursor.execute("INSERT INTO Roles VALUES (?, ?, ?, ?)", (id_perso, id_roman, nom, fonction))
                db_persos.commit()
                db_persos.close()

                message = "Personnage ajouté avec succès !"
                return redirect(url_for('accueil'))

            except Exception as e:
                message = f"Erreur : {str(e)}"

    return render_template("ajouter_perso_roman.html", message=message)

@monapp.route('/modifier/<int:id>', methods=['GET', 'POST'])
def modifier(id):
    db_persos = sqlite3.connect('personnages3.sqlite')
    db_persos.row_factory = sqlite3.Row
    cursor = db_persos.cursor()

    # Récupérer le roman
    cursor.execute("SELECT * FROM Livres WHERE id = ?", (id,))
    roman = cursor.fetchone()

    if not roman:
        return "Roman non trouvé", 404

    message = None

    #on récupère l'information sur ce qu'il faut changer
    if request.method == 'POST':
        change = request.form.get('change')

        if not change:
            message = "Veuillez entrer une nouvelle valeur."

        else:
            try:
                # Vérifier quel champ est sélectionné
                if request.form.get('titre'):
                    cursor.execute("UPDATE Livres SET titre = ? WHERE id = ?", (change, id))
                elif request.form.get('nom'):
                    cursor.execute("UPDATE Livres SET nom_principal = ? WHERE id = ?", (change, id))
                elif request.form.get('nb'):
                    cursor.execute("UPDATE Livres SET nb_chapitres = ? WHERE id = ?", (change, id))
                elif request.form.get('theme'):
                    cursor.execute("UPDATE Livres SET theme = ? WHERE id = ?", (change, id))
                elif request.form.get('epoque'):
                    cursor.execute("UPDATE Livres SET epoque = ? WHERE id = ?", (change, id))
                else:
                    message = "Aucun champ sélectionné."

                if not message:
                    db_persos.commit()
                    message = "Modification réussie !"

                    # Mettre à jour `roman` pour afficher les nouvelles données
                    cursor.execute("SELECT * FROM Livres WHERE id = ?", (id,))
                    roman = cursor.fetchone()

            except Exception as e:
                message = f"Erreur : {str(e)}"

    db_persos.close()

    return render_template("modifier.html", roman=roman, message=message)
    
monapp.run(debug=True, host = '0.0.0.0', port=3000)