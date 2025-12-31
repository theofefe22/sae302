import gui8 as gui
import rotator as rt
import sys
import socket
import threading

alfa = rt.A64()

def gestion_clients(connexion, adresse, rsa, fenetre_client):
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
                if ligne != "FIN-TRANS":
                    bloc.append(ligne)
                    continue
                
                else:    
                    print(f"Message de {adresse}")
                    print(bloc)
                    
                    dechiffre = rsa.detorage(bloc)
                    print(dechiffre)
                    
                    message = dechiffre[1]
                    print("Lor message is :", message)
                    if isinstance(message, str):
                        with open((rt.os.path.splitext(rt.os.path.basename(__file__))[0] + "messages_recus.txt"), "a", encoding = "utf-8") as h:
                            h.write(message + "\n")
                        fenetre_client.message_recu_signal.emit(message)
                    elif isinstance(message, list):
                        with open((rt.os.path.splitext(rt.os.path.basename(__file__))[0] + "messages_chiffres_recus.txt"), "a", encoding = "utf-8") as h:
                            h.write(str(message) + "\n")
                        destinataire = dechiffre[0]
                        print("Envoie du message  chiffré à :", destinataire)
                            
                        for i in range(fenetre_client.tableau_routeurs.rowCount()):
                            if fenetre_client.tableau_routeurs.item(i, 0).text() == destinataire:
                                ip_dest = fenetre_client.tableau_routeurs.item(i, 1).text()
                                port_dest = int(fenetre_client.tableau_routeurs.item(i, 2).text())
                                print(ip_dest, port_dest)

                        try:
                            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            client.connect((ip_dest, port_dest))
                                    
                            for nombre in message:
                                client.sendall((nombre + 'JEPARS').encode("utf-8"))
                            client.sendall('FIN-TRANSJEPARS'.encode("utf-8"))
                            client.close()
                        except Exception as e:
                            print("Erreur d'envoie : ", e)
                    else:
                        print("Indéterminé")
                    bloc.clear()
    finally:
        connexion.close()

def ecoute(port, rsa, fenetre_client):
    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur.bind(("0.0.0.0", port))
    serveur.listen()
    while True:
        connexion, adresse = serveur.accept()
        thread = threading.Thread(target = gestion_clients, args = (connexion, adresse, rsa, fenetre_client), daemon = True)
        thread.start()

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
    
    mon_port = rt.rds.randint(50000, 65500)
    
    # Fenêtre client
    fenetre_client = gui.Client(rsa, "Client x", rt.ip(), mon_port, ma_kp, ma_km)
    fenetre_client.showMaximized()
    
    threading.Thread(target = ecoute, args = (mon_port, rsa, fenetre_client), daemon = True).start()
    
    # Thread client
    worker = gui.ClientWorker("Client x", rt.ip(), mon_port, ma_kp, ma_km, [])
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

    # Fermeture application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
