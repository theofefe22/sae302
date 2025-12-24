import gui7 as gui
import rotator as rt
import sys
import socket
import threading

alfa = rt.A64()

def gestion_clients(connexion, adresse):
    print(f"Client connecté {adresse}")
    
    buffer = ""
    bloc = []
    
    try:
        while True:
            donnes = connexion.recv(1024)
            if not donnes:
                break
            
            buffer += donnes.decode()
            
            while "JEPARS" in buffer:
                ligne, buffer = buffer.split("JEPARS", 1)
                if ligne == "FIN-TRANS":
                    print(f"Message de {adresse}")
                    print(bloc)
                    bloc.clear()
                else:
                    bloc.append(ligne)
    finally:
        connexion.close()

# Fonction principale d'exécution
def main():
    app = gui.QApplication(sys.argv)
    app.setStyleSheet(gui.qss)

    # RSA
    rsa = rt.RSA()
    if not rt.os.path.exists(f"{rt.os.path.splitext(rt.os.path.basename(__file__))[0]}_cle_publique.pem"):
        rsa.cles(512)
        rsa.sauvegarde_cles(rt.os.path.splitext(rt.os.path.basename(__file__))[0], 7, alfa.z64_inverse('0zViens78Voirles Mousaillosn!!', 4))

    ma_cle_publique, ma_cle_privee = rsa.chargement_cles(rt.os.path.splitext(rt.os.path.basename(__file__))[0], 7, alfa.z64_inverse('0zViens78Voirles Mousaillosn!!', 4))
   
    
    port = rt.rds.randint(2000, 49999)
    
    liste_appareils = [
            ["Routeur 1", "465.15.782.16", "65300", "0x46e8765ef17b7fa9"],
            ["Routeur 2", "465.15.762.97", "65301", "0x17b7fa9"],
            ["Routeur 5", "465.15.782.13", "65301", "0x17b7fa684346859"],
            ["Client 456", "465.15.782.13", "65301", "0x17b7fa684346859"]
        ]
    
    
    
    # Fenêtre client
    fenetre_client = gui.Maitre(mon_ip = rt.ip(), mon_port = port, liste_appareils = liste_appareils, ma_cle_publique = ma_cle_publique, ma_cle_privee = ma_cle_privee)
    fenetre_client.showMaximized()
    
    

    # Fermeture application
    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()









