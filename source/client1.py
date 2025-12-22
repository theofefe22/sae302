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
        rsa.cles(256)
        rsa.sauvegarde_cles(rt.os.path.splitext(rt.os.path.basename(__file__))[0], 7, alfa.z64_inverse('0zViens78Voirles Mousaillosn!!', 4))

    ma_cle_publique, ma_cle_privee = rsa.chargement_cles(rt.os.path.splitext(rt.os.path.basename(__file__))[0], 7, alfa.z64_inverse('0zViens78Voirles Mousaillosn!!', 4))
    ma_kp = ma_cle_publique
    ma_km = ma_cle_privee
    
    # Fenêtre client
    fenetre_client = gui.Client(rsa, "Client G", rt.ip(), 48630, ma_kp, ma_km)
    fenetre_client.showMaximized()

    # Thread client
    worker = gui.ClientWorker("Client G", rt.ip(), 48630, ma_kp, ma_km, [])
    thread = gui.QThread()
    worker.moveToThread(thread)

    # On garde une référence dans la fenêtre
    fenetre_client.worker = worker
    fenetre_client.thread = thread

    # Réception des messages
    worker.message_recu.connect(fenetre_client.message_recu)
    worker.liste_routeurs.connect(fenetre_client.ajouter_routeur_tableau)

    # On démarre juste le thread (pas le worker)
    thread.start()

    
    
    """
    # Fenêtre client
    fenetre_client = gui.Client(rsa, "Client G", rt.ip(), 48630, ma_kp, ma_km)
    fenetre_client.showMaximized()

    # Thread client
    worker = gui.ClientWorker("Client G", rt.ip(), 48630, ma_kp, ma_km, [])
    thread = gui.QThread()
    worker.moveToThread(thread)

    # Réception des messages
    worker.message_recu.connect(fenetre_client.message_recu)
    worker.liste_routeurs.connect(fenetre_client.ajouter_routeur_tableau)

    # Fermeture du thread
    worker.message_recu.connect(thread.quit)
    worker.message_recu.connect(worker.deleteLater)
    thread.finished.connect(thread.deleteLater)

    # Début du thread
    thread.started.connect(worker.run)
    thread.start()
    """
    """
    # Lancer le serveur dans un thread séparé
    serveur_thread = gui.ServeurThread(fenetre_client.mon_port)  # Utilisation du port
    serveur_thread.start()
    """

    # Fermeture application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
