# BIBLIOTHEQUES
import rotator as rt
import __gui as gui
import mariadb
from mariadb import IntegrityError
import socket
import threading
import sys


# CLASSES
alfa = rt.A64()
rsa = rt.RSA()


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
            
            print(buffer)
            
            while "JEPARS" in buffer:
                ligne, buffer = buffer.split("JEPARS", 1)
                ligne = ligne.strip()
                
                if ligne == "QUIT":
                    quittage = True
                    continue
                
                if quittage and ligne != "FIN-TRANS":
                    nom = ligne              
                    historique(curseur, f"L'appareil {adresse} de nom {nom} s'est déconnecté.")
                    curseur.execute("DELETE FROM appareils WHERE nom = ?", (nom,))
                    curseur.connection.commit()
                    continue
                
                if quittage and ligne == "FIN-TRANS":
                    quittage = False
                    continue                
            
            if "Liste routeurs" in buffer:
                historique(curseur, f"L'appareil {adresse} a demandé la liste des appareils.")
                liste_appareils = recuperation(curseur)
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
                curseur.execute("SELECT id, nom FROM appareils_historique WHERE n = ? AND e = ?", (attributs['n'], attributs['e']))
                iport = curseur.fetchone()
                if iport: # MAJ des attributs
                    nom = iport[1]
                    curseur.execute("UPDATE appareils_historique SET ip = ?, port = ? WHERE id = ?", (attributs["ip"], attributs["port"], iport[0]))
                    curseur.connection.commit()
                    curseur.execute("SELECT nom, ip, port, e, n FROM appareils_historique WHERE id = ?", (iport[0],))
                    ligne = curseur.fetchone()
                    print("la ligne vaut :", ligne)
                    
                    curseur.execute("DELETE FROM appareils WHERE n = ?", (ligne[4],))
                    curseur.connection.commit() # Réinsérer l’appareil mis à jour
                    curseur.execute( "INSERT INTO appareils (nom, ip, port, e, n) VALUES (?, ?, ?, ?, ?)", ligne )
                    curseur.connection.commit()
                    
                    
                    """
                    try:
                        curseur.execute("INSERT INTO appareils (nom, ip, port, e, n) VALUES (?, ?, ?, ?, ?)", ligne)
                        curseur.connection.commit()
                    except IntegrityError as e:
                        print("Erreur INSERT appareils :", e) # par ex : remplacer plutôt que insérer
                        curseur.execute("UPDATE appareils SET nom = ?, ip = ?, port = ?, e = ?, n = ? WHERE n = ?", (*ligne, ligne[4]))
                        curseur.connection.commit()
                     """   
                        
                        
                else: # Nouvelle entrée
                    # Changement de nom
                    if "Client" in attributs["nom"]:
                        attributs["nom"] = "Client " + str(rt.rds.randint(0, 99999))
                    else:
                        attributs["nom"] = "Routeur " + str(rt.rds.randint(0, 99999))
                    nom = attributs["nom"]
                    
                    curseur.execute( "INSERT INTO appareils_historique (nom, ip, port, n, e) VALUES (?, ?, ?, ?, ?)", (nom, attributs["ip"], attributs["port"], attributs["n"], attributs["e"]) )
                    curseur.connection.commit()
                    curseur.execute( "INSERT INTO appareils (nom, ip, port, n, e) VALUES (?, ?, ?, ?, ?)", (nom, attributs["ip"], attributs["port"], attributs["n"], attributs["e"]) )
                    curseur.connection.commit()
                    
                    
                    #insertion(curseur, attributs)
                    historique(curseur, f"Insertion de {adresse} et changement de nom en {attributs['nom']}.")
                connexion.sendall(("NOUVEAU-NOM" + nom).encode("utf-8"))
                print("DEBUG n =", attributs.get("n"))
                print("DEBUG e =", attributs.get("e"))
                break
                
    except ConnectionResetError as cre:
        historique(curseur, f"Erreur de connexion de {adresse} : {cre}.")
    
    finally:
        fermer(curseur, connexion_bdd)
        connexion.close()
                
def ecoute(port):
    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur.bind(("0.0.0.0", port))
    serveur.listen()
    
    while True:
        connexion, adresse = serveur.accept()
        thread = threading.Thread(
            target = gestion_clients,
            args = (connexion, adresse),
            daemon = True)
        thread.start()

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
            n VARCHAR(2200) UNIQUE,
            e VARCHAR(2200) UNIQUE)""")
        curseur.execute(f"""CREATE TABLE IF NOT EXISTS appareils_historique (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nom VARCHAR(20),
            ip VARCHAR(15),
            port VARCHAR(5),
            n VARCHAR(2200) UNIQUE,
            e VARCHAR(2200) UNIQUE)""")
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
        curseur.execute("INSERT INTO appareils_historique (nom, ip, port, n, e) VALUES (?, ?, ?, ?, ?)", (attributs["nom"], attributs["ip"], attributs["port"], attributs["n"], attributs["e"]))
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
        appareil = {'nom': nom, 'ip': ip, 'port': port, 'n': n, 'e': e}
        liste_appareils.append(appareil)
    
    print(liste_appareils)
    return liste_appareils


def main():
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
    
    curseur, connexion_bdd = ouvrir()
    initialisation(curseur)
    historique(curseur, "Démarrage du Maître.")
    historique(curseur, f"Maître en écoute sur le port {port} de {rt.ip()}.")
    fermer(curseur, connexion_bdd)

    threading.Thread(target = ecoute, args = (port,), daemon = True).start()

    app = gui.QApplication(sys.argv)
    app.setStyleSheet(gui.qss)
    
    fenetre = gui.Maitre(mon_ip = rt.ip(), mon_port = port, liste_appareils = {}, ma_cle_publique = ma_cle_publique, ma_cle_privee = ma_cle_privee)
    fenetre.showMaximized()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
    
    
    

