# BIBLIOTHEQUES
import rotator as rt
import __gui as gui
import mariadb
import socket
import threading


# CLASSES
alfa = rt.A64()
rsa = rt.RSA()
#gui = rt.gui


# FONCIONS
def gestion_clients(connexion, adresse):
    print(f"Client connecté : {adresse}")
    curseur, connexion_bdd = ouvrir()
    historique(curseur, f"Connexion d'un appareil {adresse}.")
    buffer = ""
    bloc = []
    try:
        while True:
            donnees = connexion.recv(1024)
            if not donnees:
                break
            buffer += donnees.decode("utf-8")
            
            if "Liste routeurs" in buffer:
                historique(curseur, f"L'appareil {adresse} a demandé la liste des appareils.")
                liste_appareils = recuperation(curseur)
                print("La liste iel : ", liste_appareils)
                for appareil in liste_appareils:
                    connexion.sendall((str(appareil) + "JEPARS").encode("utf-8"))
                connexion.sendall("FIN-TRANS".encode("utf-8"))
                connexion.shutdown(socket.SHUT_WR)
                buffer = buffer.replace("Liste routeurs", "", 1)
            
            if "Demande initialisation" in buffer:
                historique(curseur, f"L'appareil {adresse} a demandé à s'initialiser au registre.")
                connexion.sendall("ACK-INITIALISATION".encode("utf-8"))
                historique(curseur, "Acceptation d'enregistrement.")
                buffer = buffer.replace("Demande initialisation", "", 1)
                param = buffer
                buffer = ""
                while "FIN-PARAM" not in param:
                    seg = connexion.recv(1024)
                    if not seg:
                        break
                    param += seg.decode("utf-8")
                param = param.replace("FIN-PARAM", "")
                param = param.split("JEPARS")
                attributs = {}
                attributs["nom"] = param[0]
                attributs["ip"] = param[1]
                attributs["port"] = param[2]
                bloc_kp = param[3].strip()
                bloc_kp = bloc_kp.lstrip("{").rstrip("}")
                paires = bloc_kp.split(",")
                for p in paires:
                    if ":" not in p:
                        continue
                    cle, valeur = p.split(":", 1)
                    cle = cle.strip().strip("'").strip('"')
                    valeur = valeur.strip().strip("'").strip('"')
                    attributs[cle] = valeur
                # Changement de nom
                if "Client" in attributs["nom"]:
                    attributs["nom"] = "Client " + str(rt.rds.randint(0, 999))
                else:
                    attributs["nom"] = "Routeur " + str(rt.rds.randint(0, 999))
                curseur.execute("SELECT id FROM appareils WHERE ip = ? AND port = ?", (attributs["ip"], attributs["port"]))
                iport = curseur.fetchone()
                if iport: # MAJ des clés
                    curseur.execute("UPDATE appareils SET n = ?, e = ? WHERE ip = ? AND port = ?", (attributs["n"], attributs["e"], attributs["ip"], attributs["port"]))
                    curseur.connection.commit()
                else: # Nouvelle entrée
                    insertion(curseur, attributs)
                curseur.execute("SELECT * FROM appareils WHERE n = ?", (attributs['n'],))
                ligne = curseur.fetchone()
                if not ligne:
                    historique(curseur, f"Changement de nom de {adresse} en {attributs['nom']}.")
                connexion.sendall(("NOUVEAU-NOM" + ligne[1]).encode("utf-8"))
                #if ligne[2] == param[1] and ligne[3] == param[2]:
                break
                
    except ConnectionResetError as cre:
        historique(curseur, f"Erreur de connexion de {adresse} : {e}.")
    
    finally:
        fermer(curseur, connexion_bdd)
        connexion.close()
                
    

def ouvrir():
    try:
        connexion_bdd = mariadb.connect(
            user = "master1",
            password = "JEsuisLEmaitre1",
            host = "127.0.0.1",
            database = "rotator",
            )
        curseur = connexion_bdd.cursor()
        print("Connecté à la base de données")
        return curseur, connexion_bdd
    except mariadb.Error as e:
        print(f"Erreur de connexion : {e}")
        exit()

def fermer(curseur, connexion_bdd):
    curseur.close()
    connexion_bdd.close()

def initialisation(curseur):
    try:
        curseur.execute(f"CREATE DATABASE IF NOT EXISTS rotator")
        curseur.execute(f"""CREATE TABLE IF NOT EXISTS appareils (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nom VARCHAR(20),
            ip VARCHAR(15),
            port VARCHAR(5),
            n VARCHAR(2200),
            e VARCHAR(2200))""")
        curseur.execute(f"ALTER TABLE appareils ADD UNIQUE (n)")
        curseur.execute(f"""CREATE TABLE IF NOT EXISTS historique (
            id INT PRIMARY KEY AUTO_INCREMENT,
            date DATETIME NOT NULL,
            description TEXT NOT NULL)""")
    except mariadb.Error as e:
        print(f"Erreur d'initialisation : {e}")

def insertion(curseur, attributs: dict):
    try:
        curseur.execute("INSERT INTO appareils (nom, ip, port, n, e) VALUES (?, ?, ?, ?, ?)", (attributs["nom"], attributs["ip"], attributs["port"], attributs["n"], attributs["e"]))
        curseur.connection.commit()
        print(f"Ajout de données à la base appareils")
    except mariadb.Error as e:
        print(f"Erreur d'ajout : {e}")

def historique(curseur, description: str):
    try:
        curseur.execute("INSERT INTO historique (date, description) VALUES (NOW(), ?)", (description,))
        curseur.connection.commit()
        print(f"Ajout de données à l'historique")
    except mariadb.Error as e:
        print(f"Erreur d'ajout : {e}")

def recuperation(curseur):
    curseur.execute(f"SELECT id, nom, ip, port, n, e FROM appareils")
    liste_appareils = []
    
    for (id, nom, ip, port, n, e) in curseur:
        print(id, nom, ip, port, n, e)
        appareil = {'nom': nom, 'ip': ip, 'port': port, 'n': n, 'e': e}
        print(appareil)
        liste_appareils.append(appareil)
    
    print(liste_appareils)
    return liste_appareils


# GESTION DE MES CLES RSA
K_ECDHE = ('0z0 ASDMdcYYcPf0kDSkQ99OrxxeXYblyCPtECL0FmSbh', '0zWZ5RZZ6bFxucTPIb8mvHPOEyYc4CCTbH31B3ergWmJ9')

if not rt.os.path.exists(f"{rt.os.path.splitext(rt.os.path.basename(__file__))[0]}_cle_publique.pem"):
    rsa.cles(683)
    curseur, connexion_bdd = ouvrir()
    historique(curseur, "Création des clés RSA du Maître.")
    fermer(curseur, connexion_bdd)
    print(rsa.Km)
    print(rsa.Kp)
    rsa.sauvegarde_cles(rt.os.path.splitext(rt.os.path.basename(__file__))[0], 7, alfa.z64_inverse('0z0 ASDMdcYYcPf0kDSkQ99OrxxeXYblyCPtECL0FmSbh', 7))

ma_cle_publique, ma_cle_privee = rsa.chargement_cles(rt.os.path.splitext(rt.os.path.basename(__file__))[0], 7, alfa.z64_inverse(K_ECDHE[0], 7))

print(f"Ma clé publique RSA est : {ma_cle_publique}")
print(f"Ma clé privée RSA est : {ma_cle_privee}")





port = rt.rds.randint(2000, 49999)
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind(("0.0.0.0", port))
serveur.listen()

curseur, connexion_bdd = ouvrir()
initialisation(curseur)
historique(curseur, "Démarrage du Maître.")
historique(curseur, f"Maître en écoute sur le port {port} de {rt.ip()}.")
fermer(curseur, connexion_bdd)

while True:
    connexion, adresse = serveur.accept()
    thread = threading.Thread(
        target = gestion_clients,
        args = (connexion, adresse),
        daemon = True)
    thread.start()










"""


# BOUCLE PRINCIPALE
while True:
    fenetre = gui.Maitre() 
    reponse = None
    while reponse is None:
        reponse = serveur.message_client()
    # BOUCLES DES REPONSES POSSIBLES
    # Initialisation routeur
    if reponse == "Je suis nouveau":
        print("Phase d'initialisation d'un routeur.")
        cs.send("Demande ID".encode())
    # Demande la liste des emachines
    elif reponse == "Je veux liste machines":
        print("Phase d'envoie d'informations concernant les machines")
    
    
"""
   


