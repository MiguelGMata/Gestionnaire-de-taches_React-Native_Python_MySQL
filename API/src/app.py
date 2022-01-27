from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin


from config import connexion

app = Flask(__name__)

CORS(app, resources={r"/todo/*": {"origins": "http://localhost:3000/" }})

mysql = connexion()

#-----------------------------------GET TOUTES LES TACHES ACCUEIL-----------------------------------------------
@app.route('/todo/tache', methods=['GET'])
def listar_cursos():
    try:
        cur =  mysql.cursor()
        sql = "SELECT id, nom, description FROM taches ORDER BY nom ASC"
        cur.execute(sql)
        datos = cur.fetchall()
        taches = []
        for fila in datos:
            tache = {'id': fila[0], 'nom': fila[1], 'description': fila[2]}
            taches.append(tache)
        return jsonify({'Taches': taches, 'mensaje': "Liste de taches.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})

    
#-----------------------------------POST UNE TACHE-----------------------------------------------
@cross_origin
@app.route('/todo/tache', methods=['POST'])
def creer_taches():
        try:
            data = (request.json['nom'], request.json['description'])
            cur = mysql.cursor()
            cur.execute('INSERT INTO taches (nom, description) VALUES (%s,%s)', data)
            mysql.commit()
            return jsonify({'mensage': 'Tâches ajoutée', 'exito': True})#, redirect(url_for('Index'))     
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})

@cross_origin
@app.route('/todo/taches', methods=['POST'])
def creer_tache():
    try: 
        cur =  mysql.cursor()
        cur.execute("INSERT INTO taches (nom, description) VALUES ('{0}', '{1}')".format(request.json['nom'], request.json['description']))
        mysql.commit() ## Confirmation de l'action d'insertion.
        return jsonify({'mensaje': 'Tâches ajoutée', 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


#---------------------------------------GET TOUTES LES TACHES-------------------------------------------

@app.route('/todo/taches', methods=['GET'])
def get_tâches():
    try:
        cur =  mysql.cursor()
        cur.execute("SELECT id, nom, description FROM taches") #On execute la requête 
        data = cur.fetchall() #response de mysql
        taches = []
        for file in data:
            tache = {'id': file[0], 'nom': file[1], 'description': file[2]}
            taches.append(tache)
        #print(taches,'------>')
        return jsonify({'Taches': taches, 'mensage': "Liste de tâches.", 'exito': True})#retour de JSON avec la liste
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


#-----------------------------------------GET TACHE ID-----------------------------------------
@cross_origin
@app.route('/todo/tache/<id>', methods=['GET'])
def get_tâche_id(id):
    try:
        data = (id)
        cur = mysql.cursor()
        sql = "SELECT * FROM taches WHERE id ='{0}'".format(id)
        cur.execute(sql)
        data = cur.fetchone()
        if data != None:
            tache = {'id': data[0], 'nom': data[1], 'description': data[2]}
            return jsonify({'tache': tache, 'mensage': 'Tâche trouvée'})
        else:
            return jsonify({'mensage': 'Erreur, tâche non trouvée'})
    except Exception as ex:
        return jsonify({'mensage': 'Erreur'})

#------------------------------------------DELETE TACHE----------------------------------------
@cross_origin
@app.route('/todo/tache/<id>', methods=['DELETE'])
def delete_tache_id(id):
    cur = mysql.cursor()
    cur.execute("DELETE FROM taches WHERE id = {0}".format(id))
    mysql.commit()
    return jsonify({'mensage': 'tâche effacée'})

#-----------------------------------------UPDATE TACHE-----------------------------------------
@cross_origin
@app.route('/todo/tache/<id>', methods=['POST'])
def update_tache_id(id):
    try:
        if request.method =='POST':
            nom = request.json['nom']
            description = request.json['description']
            cur = mysql.cursor()
            cur.execute("""
                UPDATE taches 
                SET nom = %s, 
                description = %s
                WHERE id = %s
                """, ( nom, description, id))
            
            sql = "SELECT * FROM taches WHERE id ='{0}'".format(id)
            cur.execute(sql)
            data = cur.fetchone()
            print(data)
            mysql.commit()
            tache = {'id': data[0], 'nom': data[1], 'description': data[2]}
            return jsonify({'tache': tache,'mensage': 'Tâche modifiée avec succès'})#, redirect(url_for('Index'))   
        else:
            return jsonify({'mensage': 'Erreur, tâche non trouvée'})
    except Exception as ex:
        return jsonify({'mensage': 'Erreur'})

#----------------------------PAGE ERREUR 404------------------------------------------------------
def page_erreur(error):
    return"<h1>Erreur 404, page non trouvée.</h1>", 404

if __name__ == '__main__':
    app.register_error_handler(404, page_erreur)
    app.run(port = 3000, debug = True)
