# BIBLIOTHEQUES
import rotator as rt
import __gui as gui


# CLASSES
alfa = rt.A64()
rsa = rt.RSA()
#gui = rt.gui






# GESTION DE MES CLES RSA
K_ECDHE = ('0z0 ASDMdcYYcPf0kDSkQ99OrxxeXYblyCPtECL0FmSbh', '0zWZ5RZZ6bFxucTPIb8mvHPOEyYc4CCTbH31B3ergWmJ9')

if not rt.os.path.exists(f"{rt.os.path.splitext(rt.os.path.basename(__file__))[0]}_cle_publique.pem"):
    rsa.cles(683)
    print(rsa.Km)
    print(rsa.Kp)
    rsa.sauvegarde_cles(rt.os.path.splitext(rt.os.path.basename(__file__))[0], 7, alfa.z64_inverse('0z0 ASDMdcYYcPf0kDSkQ99OrxxeXYblyCPtECL0FmSbh', 7))

ma_cle_publique, ma_cle_privee = rsa.chargement_cles(rt.os.path.splitext(rt.os.path.basename(__file__))[0], 7, alfa.z64_inverse(K_ECDHE[0], 7))

print(f"Ma clé publique RSA est : {ma_cle_publique}")
print(f"Ma clé privée RSA est : {ma_cle_privee}")















#fenetre = gui.maitre()

# PARAMETERES
bdd_hote = "localhost"
bdd_utilisateur = "master1"
bdd_mdp = "JEsuisLEmaitre1"
bdd_bdd = "rotator_"+"sae302_tests_01"
bdd_table = "Routeurs2"
mon_ip = rt.ip()
port = 50000
serveur = rt.Serveur(port)
print(f"Le maître est en écoute sur le port {port} de l'IP {mon_ip}")
#cs, adresse = serveur.ecoute()


# BASE DE DONNEES
bdd = rt.BDD(bdd_hote, bdd_utilisateur, bdd_mdp, bdd_bdd)
bdd.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {bdd_bdd}")
bdd.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {bdd_table} (
    id INT PRIMARY KEY AUTO_INCREMENT,
    ip VARCHAR(15),
    port VARCHAR(5),
    n VARCHAR(2200),
    e VARCHAR(2200))""")




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
   


