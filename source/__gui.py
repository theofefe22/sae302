import sys
import threading
import rotator as rt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
#from maitre import ouvrir, fermer, recuperation


import time
import socket



with open("style.qss", "r") as file:
    qss = file.read()


class Progression(QDialog):
    def __init__(self, pourcentage: int = 0, parent = None):
        super().__init__(parent)
        
        self.__pourcentage = pourcentage

        self.setWindowTitle("Chiffrement du message")
        self.resize(200, 50)
        
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(self.__pourcentage)
        print(f"Le chiffrement du message est à {self.pourcentage} %")
        
        layout = QVBoxLayout()
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)
        
    @property
    def pourcentage(self):
        return self.__pourcentage
    
    @pourcentage.setter
    def pourcentage(self, pourcentage: int):
        if isinstance(pourcentage, int):
            self.__pourcentage = pourcentage
            self.progress_bar.setValue(self.__pourcentage)
            print(f"Le chiffrement du message est à {self.pourcentage} %")
        else:
            raise ValueError("Le format n'est pas correcte.")       


class Client(QTabWidget):
    def __init__(self, rsa, mon_nom: str, mon_ip: str, mon_port: int, ma_kp: dict, ma_km: dict, parent = None):
        super(Client, self).__init__(parent)
        
        self.onglet1 = QWidget()
        self.onglet2 = QWidget()
        self.onglet3 = QWidget()
        self.onglet4 = QWidget()
        
        self.addTab(self.onglet1, "Page principale")
        self.addTab(self.onglet2, "Envoyer un message")
        self.addTab(self.onglet3, "Messages reçus")
        self.addTab(self.onglet4, "Liste des routeurs")
        
        self.cles_publiques = []
        self.mon_port = mon_port
        self.ip_maitre = QLineEdit(mon_ip)
        
        self.creation_onglet1(mon_nom, mon_ip, mon_port, ma_kp, ma_km)
        self.creation_onglet2(rsa)
        self.creation_onglet3()
        self.creation_onglet4()
        
        self.setWindowTitle("ROTATOR v1 - Client")
        self.setWindowIcon(QIcon("logo_rotator.png"))
        
    def creation_onglet1(self, mon_nom: str, mon_ip: str, mon_port: int, ma_kp: dict, ma_km: dict):
        """
        Création de la page principale
        
        Attributs :
            mon_nom (str) : Nom donné par le Maître
            mon_ip (str) : Adresse IP
            mon_port (int) : Port d'écoute
            ma_kp (dict) : Clé publique RSA
            ma_km (dict) : Clé privée RSA
        """
        def initialiser():
            """Initialisation de l'appareil"""
            ip_maitre = element_ip_maitre.text()
            if element_port_maitre.text() == "":
                port_maitre = 57000
            else:
                port_maitre = int(element_port_maitre.text())
            parametres = [mon_nom, mon_ip, str(mon_port), str(ma_kp)]
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client.connect((ip_maitre, port_maitre))
            except:
                print("Connexion impossible")
                element_ip_maitre.setStyleSheet("background-color: #E3492D")
                element_port_maitre.setStyleSheet("background-color: #E3492D")
                return
            client.sendall('Demande initialisation'.encode("utf-8"))
            
            reponse = b''
            if b"FIN-TRANS" not in reponse:
                segment = client.recv(1024)
                if not segment:
                    return
                reponse += segment
                
                if b"ACK-INITIALISATION" in reponse:
                    for element in parametres:
                        client.sendall((element + "JEPARS").encode("utf-8"))
                    client.sendall("FIN-PARAM".encode("utf-8"))
                reponse = client.recv(1024)
                if b"Client" in reponse:
                    try:
                        self.mon_nom = reponse.split(b"NOUVEAU-NOM")[1].decode("utf-8")
                        print("Nouveau nom :", self.mon_nom)
                        element_nom.setText(self.mon_nom)
                    except:
                        self.mon_nom = self.mon_nom
        
        def fermer(self):
            print("Fermeture de la fenêtre")
            sys.exit()
        
        def demander():
            ip_maitre = element_ip_maitre.text()
            if element_port_maitre.text() == "":
                port_maitre = 57000
            else:
                port_maitre = int(element_port_maitre.text())
            print(f"Connexion au maître sur le port {port_maitre} de {ip_maitre}")
            
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client.connect((ip_maitre, port_maitre))
            except:
                print("Connexion impossible")
                element_ip_maitre.setStyleSheet("background-color: #E3492D")
                element_port_maitre.setStyleSheet("background-color: #E3492D")
                return
            client.sendall('Liste routeurs'.encode("utf-8"))
            element_ip_maitre.setStyleSheet("")
            element_port_maitre.setStyleSheet("")
            print('Demande de la liste des appareils en cours...')
            
            reponse = b''
            while b"FIN-TRANS" not in reponse:
                segment = client.recv(1024)
                if not segment:
                    break
                reponse += segment
            
            reponse_str = reponse.decode("utf-8")
            element = reponse_str.split("JEPARS")
            # Moins blocs osef
            blocs_filtres = []
            for b in element:
                b = b.strip()
                if b and b != "FIN-TRANS":
                    blocs_filtres.append(b)
            # Conversion en dict
            liste_dicts = []
            for brut in blocs_filtres:
                if brut.startswith("{") and brut.endswith("}"):
                    brut = brut[1:-1]
                paires = brut.split(",")
                d = {}
                for p in paires:
                    cle, valeur = p.split(":", 1)
                    cle = cle.strip().strip("'").strip('"')
                    valeur = valeur.strip().strip("'").strip('"')
                    d[cle] = valeur
                liste_dicts.append(d)
            self.tableau_routeurs.setRowCount(0)
            self.cles_publiques = liste_dicts
            print("Liste des appareils reçus :")
            print(self.cles_publiques)
            self.worker.appareils = self.cles_publiques
            self.worker.liste_appareils()
            self.maj_appareils()
        
        self.mon_nom = mon_nom
        disposition = QVBoxLayout()
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        #datetime_edit = QDateTimeEdit()
        
        titre1 = QLabel("Paramètres primaires :")
        titre1.setObjectName("h1")
        titre1.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        disposition_parametres = QFormLayout()
        
        label_nom = QLabel("Nom :")
        element_nom = QLineEdit(self.mon_nom)
        element_nom.setReadOnly(True)
        
        label_mon_ip = QLabel("Adresse IP :")
        element_mon_ip = QLineEdit(mon_ip)
        element_mon_ip.setReadOnly(True)
        
        label_mon_port = QLabel("Port :")
        element_mon_port = QLineEdit(str(mon_port))
        validateur = QIntValidator(0, 999999)
        element_mon_port.setValidator(validateur)
        
        label_ma_kp = QLabel("Clé publique RSA :")
        element_ma_kp = QPlainTextEdit(str(ma_kp))
        element_ma_kp.setReadOnly(True)
        
        label_ma_km = QLabel("Clé privée RSA :")
        element_ma_km = QPlainTextEdit(str(ma_km))
        element_ma_km.setReadOnly(True)
        
        element_ma_kp.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        element_ma_km.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        
        disposition_parametres.addRow(label_nom, element_nom)
        disposition_parametres.addRow(label_mon_ip, element_mon_ip)
        disposition_parametres.addRow(label_mon_port, element_mon_port)
        disposition_parametres.addRow(label_ma_kp, element_ma_kp)
        disposition_parametres.addRow(label_ma_km, element_ma_km)
                
        titre2 = QLabel("Paramètres du Maître :")
        titre2.setObjectName("h1")
        
        disposition_parametres2 = QFormLayout()
        
        label_nom_maitre = QLabel("Nom :")
        element_nom_maitre = QLineEdit("Maître")
        element_nom_maitre.setReadOnly(True)
        
        label_ip_maitre = QLabel("Adresse IP :")
        element_ip_maitre = QLineEdit("")
        
        label_port_maitre = QLabel("Port :")
        element_port_maitre = QLineEdit("")
        validateur_maitre = QIntValidator(0, 999999)
        element_port_maitre.setValidator(validateur_maitre)
        
        disposition_parametres2.addRow(label_nom_maitre, element_nom_maitre)
        disposition_parametres2.addRow(label_ip_maitre, element_ip_maitre)
        disposition_parametres2.addRow(label_port_maitre, element_port_maitre)
        
        disposition_boutons = QHBoxLayout()        
        bouton_enregistrer = QPushButton("Enregistrer les paramètres")
        bouton_enregistrer.setFixedHeight(40)
        bouton_enregistrer.setObjectName("bouton-bleu")
        
        bouton_demande = QPushButton("Demander la liste des routeurs")
        bouton_demande.setFixedHeight(40)
        bouton_demande.setObjectName("bouton-rouge")
        
        bouton_fermer = QPushButton("Fermer l'application")
        bouton_fermer.setFixedHeight(40)
        bouton_fermer.setObjectName("bouton-rouge")

        disposition_boutons.addWidget(bouton_enregistrer)
        disposition_boutons.addWidget(bouton_demande)
        disposition_boutons.addWidget(bouton_fermer)
        
        bouton_enregistrer.clicked.connect(initialiser)
        bouton_demande.clicked.connect(demander)
        bouton_fermer.clicked.connect(fermer)
        
        disposition.addWidget(titre1)
        disposition.addSpacing(10)
        disposition.addLayout(disposition_parametres)
        disposition.addSpacing(10)
        disposition.addWidget(titre2)
        disposition.addSpacing(10)
        disposition.addLayout(disposition_parametres2)
        disposition.addLayout(disposition_boutons)
        
        content_widget = QWidget()
        content_widget.setLayout(disposition)
        scroll_area.setWidget(content_widget)
        
        disposition_scroll = QVBoxLayout()
        disposition_scroll.addWidget(scroll_area)

        self.onglet1.setLayout(disposition_scroll)
        
    def creation_onglet2(self, rsa):
        """
        Onglet 2 de l'interface client. Permet l'envoie de messages privés.
        """
        def choix_client() -> str:
            """
            Choix du client
            
            Renvoie :
                client (str) : Client choisi
            """
            client = self.destinataire.currentText()
            if client == "Client A":
                print(f"Vous allez envoyer votre message à {client}")
            elif client == "Client B":
                print(f"Vous allez envoyer votre message à {client}")
            else:
                action = "Aucune sélection valide"
            return client
                    
        def maj_label_nb_routeurs(nb_routeurs: int) -> None:
            """
            Met à jour le nombre de routeurs
            
            Arguments :
                nb_routeurs (int) : Nombre de routeurs
            """
            self.nb_routeurs = nb_routeurs
            if nb_routeurs < 2 :
                label_curseur.setText(f"Votre message va passer par {str(nb_routeurs)} routeur")
            else:
                label_curseur.setText(f"Votre message va passer par {str(nb_routeurs)} routeurs")
                
        def raz_texte():
            """Annule l'envoie d'un message"""
            texte.setText("")
            self.destinataire.setCurrentIndex(0)
            curseur_nb_routeurs.setValue(0)

        def envoyer():
            """Envoie d'un message"""
            self.destinataire = choix_client()
            if self.destinataire == "Choisissez un client":
                raz_texte()
                return
            message = texte.toPlainText()
            print(message)
            
            dialog_progression = Progression(0, self)
            dialog_progression.show()
            
            if self.etat == 0:
                print("Mode auto")
            
                routeurs = ["Routeur 1", "Routeur 2"]
                routeurs_aleatoire = []
            
                for i in range(0, self.nb_routeurs):
                    routeurs_aleatoire.append(routeurs[rt.rds.randint(0, len(routeurs) - 1)])
                print(routeurs_aleatoire)
            
            else:
                
                #route = self.cles_publiques.currentText()
                route = self.liste_passages.currentText()
                routeurs_aleatoire = route.split("->")
                print(routeurs_aleatoire)
            
            passage = tuple(routeurs_aleatoire + [self.destinataire])
            print(f"Le message va passer par {passage}")
            
            dialog_progression.pourcentage = 50
            
            chiffre, destinataire = rsa.torage(message, passage, self.cles_publiques)
            dest = destinataire['nom']
            print(dest, chiffre)
            
            adresse_destinataire = destinataire['ip']
            port_receveur = destinataire['port']
            
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((adresse_destinataire, port_receveur))
            
            for nombre in chiffre:
                client.sendall((nombre + 'JEPARS').encode("utf-8"))
            client.sendall('FIN-TRANSJEPARS'.encode("utf-8"))
            client.close()
            
            print(f"Message envoyé à {destinataire}")
            dialog_progression.pourcentage = 100
            dialog_progression.close()
            raz_texte()
            return
        
        def manuel(etat):
            self.etat = etat
            if self.etat == 0:
                curseur_nb_routeurs.setEnabled(True)
                self.liste_passages.setEnabled(False)
            else:
                curseur_nb_routeurs.setEnabled(False)
                self.liste_passages.setEnabled(True)

        disposition = QVBoxLayout()
        self.etat = 0
        
        label_destinataire = QLabel("Envoyer le message à :")
        self.destinataire = QComboBox()
        self.destinataire.addItem("Choisissez un client")
        self.destinataire.currentTextChanged.connect(choix_client)
        disposition_destinataire = QFormLayout()
        disposition_destinataire.addRow(label_destinataire, self.destinataire)
        
        texte = QTextEdit()
        texte.setPlaceholderText("Saisissez votre message ici…")
        
        separateur1 = QFrame()
        separateur1.setFrameShape(QFrame.Shape.HLine)
        separateur1.setFrameShadow(QFrame.Shadow.Sunken)
        
        mode = QCheckBox("Mode manuel")
        mode.stateChanged.connect(manuel)
        
        disposition_routeur = QHBoxLayout()
        
        liste_appareils = [cle["nom"] for cle in self.cles_publiques]
        
        self.liste_passages = QComboBox()
        self.liste_passages.addItem("Choisissez un passage")
        self.liste_passages.setEnabled(False)
        
        #generer_permutations(self.cles_publiques)
        
        separateur2 = QFrame()
        separateur2.setFrameShape(QFrame.Shape.HLine)
        separateur2.setFrameShadow(QFrame.Shadow.Sunken)
        
        curseur_nb_routeurs = QSlider(Qt.Orientation.Horizontal)
        curseur_nb_routeurs.setMinimum(0)
        curseur_nb_routeurs.setMaximum(10)
        label_curseur = QLabel(f"Votre message va passer par {str(curseur_nb_routeurs.value())} routeur")
        self.nb_routeurs = 0
        curseur_nb_routeurs.valueChanged.connect(maj_label_nb_routeurs)
        
        separateur3 = QFrame()
        separateur3.setFrameShape(QFrame.Shape.HLine)
        separateur3.setFrameShadow(QFrame.Shadow.Sunken)

        disposition_boutons = QHBoxLayout()
        
        self.bouton_envoyer = QPushButton("Envoyer le message")
        self.bouton_envoyer.setFixedHeight(40)
        self.bouton_envoyer.setObjectName("bouton-bleu")
        
        bouton_annuler = QPushButton("Annuler")
        bouton_annuler.setFixedHeight(40)
        bouton_annuler.setObjectName("bouton-rouge")
        
        disposition_boutons.addWidget(self.bouton_envoyer)
        self.bouton_envoyer.clicked.connect(envoyer)
        disposition_boutons.addWidget(bouton_annuler)
        bouton_annuler.clicked.connect(raz_texte)
        
        disposition.addLayout(disposition_destinataire)
        disposition.addWidget(texte)
        disposition.addSpacing(10)
        disposition.addWidget(separateur1)
        disposition.addSpacing(10)
        disposition.addWidget(mode)
        
        disposition.addWidget(self.liste_passages)
        
        disposition.addWidget(separateur2)
        disposition.addSpacing(10)
        disposition.addWidget(label_curseur)
        disposition.addWidget(curseur_nb_routeurs)
        disposition.addSpacing(10)
        disposition.addWidget(separateur3)
        disposition.addSpacing(10)
        disposition.addLayout(disposition_boutons)
        
        self.onglet2.setLayout(disposition)
        
    def creation_onglet3(self):
        
        self.tableau_messages = QTableWidget()
        self.tableau_messages.setRowCount(0)
        self.tableau_messages.setColumnCount(1)
        self.tableau_messages.setHorizontalHeaderLabels(["Messages reçus"])
        
        disposition = QGridLayout()
        disposition.addWidget(self.tableau_messages)
        self.onglet3.setLayout(disposition)
        
        self.tableau_messages.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tableau_messages.horizontalHeader().setStretchLastSection(True) 
        
    def creation_onglet4(self):
        self.tableau_routeurs = QTableWidget()
        self.tableau_routeurs.setRowCount(0)
        self.tableau_routeurs.setColumnCount(5)
        self.tableau_routeurs.setHorizontalHeaderLabels(["Routeur", "Adresse IP", "Port", "Clé publique RSA (n)", "Clé publique RSA (e)"])
        
        disposition = QGridLayout()
        disposition.addWidget(self.tableau_routeurs)
        self.onglet4.setLayout(disposition)
        
        self.tableau_routeurs.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tableau_routeurs.horizontalHeader().setStretchLastSection(True)
        
    def message_recu(self, message: str):
        """Ajoute un message dans le tableau"""
        ligne = self.tableau_messages.rowCount()
        self.tableau_messages.insertRow(ligne)
        item = QTableWidgetItem(message)
        self.tableau_messages.setItem(ligne, 0, item)
    
    def ajouter_routeur_tableau(self, routeur: dict):
        """
        Ajoute un routeur dans le tableau.
           routeur doit être un dictionnaire avec les clés : 'nom', 'n', 'e', éventuellement 'ip' et 'port'.
        """        
        ligne = self.tableau_routeurs.rowCount()
        self.tableau_routeurs.insertRow(ligne)

        item_nom = QTableWidgetItem(routeur.get('nom', ''))
        self.tableau_routeurs.setItem(ligne, 0, item_nom)

        item_ip = QTableWidgetItem(routeur.get('ip', ''))
        self.tableau_routeurs.setItem(ligne, 1, item_ip)

        item_port = QTableWidgetItem(str(routeur.get('port', '')))
        self.tableau_routeurs.setItem(ligne, 2, item_port)

        item_n = QTableWidgetItem(routeur.get('n', ''))
        self.tableau_routeurs.setItem(ligne, 3, item_n)
        
        item_e = QTableWidgetItem(routeur.get('e', ''))
        self.tableau_routeurs.setItem(ligne, 4, item_e)
        
        self.liste_passages.addItem(routeur['nom'])
        
        if routeur['nom'].startswith("Client"):
            self.destinataire.addItem(routeur['nom'])

    def liste_routeurs(self, routeurs: list):
        """Ajoute les routeurs dans le tableau"""
        for routeur in routeurs :
            ligne = self.tableau_routeurs.rowCount()
            self.tableau_routeurs.insertRow(ligne)
            item = QTableWidgetItem(routeur)
            self.tableau_routeurs.setItem(ligne, 0, item)
    
    def maj_appareils(self):
        """
        self.liste_passages.clear()
        self.destinataire.clear()
        self.liste_passages.addItem("Choisissez un passage")
        self.destinataire.addItem("Choisissez un destinataire")
        
        permutations = self.generer_permutations(clients)
        for p in permutations:
            self.liste_passages.addItem(p)
        """    
        # vider les combos
        self.destinataire.clear()
        self.liste_passages.clear()

        self.destinataire.addItem("Choisissez un destinataire")
        self.liste_passages.addItem("Choisissez un passage")

        # --- Clients uniquement pour destinataire ---
        clients = [r['nom'] for r in self.cles_publiques if r['nom'].startswith("Client")]

        for nom in clients:
            self.destinataire.addItem(nom)

        # --- Tous les appareils pour liste_passages ---
        appareils = [r['nom'] for r in self.cles_publiques]

        # Ajouter les appareils bruts
        for nom in appareils:
            self.liste_passages.addItem(nom)

        # Générer permutations
        permutations = self.generer_permutations(appareils)

        for p in permutations:
            self.liste_passages.addItem(p)

            
            
            
            
    
    def generer_permutations(self, elements, chemin = None, resultat = None):
        if chemin == None:
            chemin = []
        if resultat == None:
            resultat = []
        if chemin:
            resultat.append("->".join(chemin))
        for i, element in enumerate(elements):
            reste = elements[:i] + elements[i+1:]
            self.generer_permutations(reste, chemin + [element], resultat)
        return resultat




class Maitre(QTabWidget):
    def __init__(self, mon_ip: str, mon_port: int, liste_appareils: dict, ma_cle_publique, ma_cle_privee, parent = None):
        super(Maitre, self).__init__(parent)
        
        self.timer = QTimer()
        #self.timer.timeout.connect(self.maj_bdd)
        self.timer.start(120_000)
        
        self.mon_ip = mon_ip
        self.mon_port = mon_port
        self.liste_appareils = liste_appareils
        self.ma_cle_publique = ma_cle_publique
        self.__ma_cle_privee = ma_cle_privee
        
        self.onglet1 = QWidget()
        self.onglet2 = QWidget()
        self.onglet3 = QWidget()
        
        self.addTab(self.onglet1, "Page principale")
        self.addTab(self.onglet2, "Liste des routeurs")
        self.addTab(self.onglet3, "Liste des clients")

        self.creation_onglet1()
        self.creation_onglet2()
        self.creation_onglet3()
        
        self.setWindowTitle("ROTATOR v1 - Maître")
        self.setWindowIcon(QIcon("logo_rotator.png"))
        
    def creation_onglet1(self):
        disposition = QFormLayout()
        
        titre1 = QLabel("Paramètres primaires :")
        titre1.setObjectName("h1")
        titre1.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        label_nom = QLabel("Nom :")
        element_nom = QLineEdit("Maitre")
        element_nom.setReadOnly(True)
        
        label_maitre_ip = QLabel("Adresse IP :")
        element_maitre_ip = QLineEdit(self.mon_ip)
        element_maitre_ip.setReadOnly(True)
        
        label_maitre_port = QLabel("Port :")
        element_maitre_port = QLineEdit("16540")
        element_maitre_port.setReadOnly(True)
        
        label_maitre_kp = QLabel("Clé publique RSA :")
        element_maitre_kp = QPlainTextEdit(str(self.ma_cle_publique))
        element_maitre_kp.setReadOnly(True)
        
        label_maitre_km = QLabel("Clé privée RSA :")
        element_maitre_km = QPlainTextEdit(str(self.__ma_cle_privee))
        element_maitre_km.setReadOnly(True)
        
        element_maitre_kp.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        element_maitre_km.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        
        bouton_fermer = QPushButton("Fermer")
        bouton_fermer.setMaximumWidth(200)
        bouton_fermer.setObjectName("bouton-rouge")

        disposition.addRow(titre1)
        disposition.addRow(label_nom, element_nom)
        disposition.addRow(label_maitre_ip, element_maitre_ip)
        disposition.addRow(label_maitre_port, element_maitre_port)
        disposition.addRow(label_maitre_kp, element_maitre_kp)
        disposition.addRow(label_maitre_km, element_maitre_km)
        disposition.addRow(bouton_fermer)
        bouton_fermer.clicked.connect(self.slot_fermer)

        self.onglet1.setLayout(disposition)
        disposition.setVerticalSpacing(10)
        
    def creation_onglet2(self):
        tableau_routeurs = QTableWidget()
        tableau_routeurs.setRowCount(len(self.liste_appareils))
        tableau_routeurs.setColumnCount(5)
        tableau_routeurs.setHorizontalHeaderLabels(["Routeur", "Adresse IP", "Port", "Clé publique RSA (n)", "Clé publique RSA (e)"])
        
        for ligne, valeurs in enumerate(self.liste_appareils):
            for colonne, valeur in enumerate(valeurs):
                item = QTableWidgetItem(valeur)
                tableau_routeurs.setItem(ligne, colonne, item)


        disposition = QGridLayout()
        disposition.addWidget(tableau_routeurs)
        self.onglet2.setLayout(disposition)
        
        tableau_routeurs.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        tableau_routeurs.horizontalHeader().setStretchLastSection(True)
    
    def creation_onglet3(self):
        self.tableau_clients = QTableWidget()
        self.tableau_clients.setRowCount(0)
        self.tableau_clients.setColumnCount(5)
        self.tableau_clients.setHorizontalHeaderLabels(["Routeur", "Adresse IP", "Port", "Clé publique RSA (n)", "Clé publique RSA (e)"])
        
        disposition = QGridLayout()
        disposition.addWidget(self.tableau_clients)
        self.onglet3.setLayout(disposition)
        
        self.tableau_clients.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tableau_clients.horizontalHeader().setStretchLastSection(True)
    
    def slot_fermer(self):
        print("Fermeture de la fenêtre")
        sys.exit()

    def maj_bdd(self):
        ouvrir()
        appareils = recuperation()
        
        self.tableau_routeurs.setRowCount(0)
        self.tableau_clients.setRowCount(0)
        self.destinataire.clear()
        
        for appareil in appareils:
            self.ajouter_appareil_tableau(appareil)

    def ajouter_routeur_tableau(self, liste_appareils: dict):
        """
        Ajoute un routeur dans le tableau.
        
        Arguments :
            liste_appareils : Liste des appareils
        """        
        if appareil["nom"].startswith("Routeur"):
            tableau = self.tableau_routeurs
        
        elif appareil["nom"].startswith("Client"):
            tableau = self.tableau_clients
        
        ligne = tableau.rowCount()
        tableau.insertRow(ligne)
        
        tableau.setItem(ligne, 0, QTableWidgetItem(appareil.get("nom", "")))
        tableau.setItem(ligne, 1, QTableWidgetItem(appareil.get("ip", "")))
        tableau.setItem(ligne, 2, QTableWidgetItem(str(appareil.get("port", ""))))
        tableau.setItem(ligne, 3, QTableWidgetItem(appareil.get("n", "")))
        tableau.setItem(ligne, 4, QTableWidgetItem(appareil.get("e", "")))



class ClientWorker(QObject):
    message_recu = pyqtSignal(str)
    liste_routeurs = pyqtSignal(object)

    def __init__(self, nom, ip, port, kp, km, appareils):
        super().__init__()
        self.nom = nom
        self.ip = ip
        self.port = port
        self.kp = kp
        self.km = km
        self.appareils = appareils

    def message_recus(self):
        """Réception et affichage des messages reçus"""
        messages = ["Salut !", "Un deuxième message", "Encore un message"]
        for msg in messages:
            time.sleep(2)
            self.message_recu.emit(msg)
        
    def liste_appareils(self):
        """Réception et affichage des appareils connecté"""
        """
        cle_public_r1 = {'nom' : 'Routeur 1', 'n': '0x5d24dc9b28a8cb3af3ff79147ae18bedb25a6398f9027a9f537cf19b6c409556eaf9c6cceb262b6c4704d50536829bbbdf820b8eeb7861929b242baba6e75f9f73c7593151995800feef75e2c451de1af3d23fc5416000de68ed3f2922b71d43123cf7ae08338458fc8aef0d55c090f5f21eddc432677a692d057033bc92e1e170e688be39b6a3e6eaf5b64dbad1e9620dfa05400356722c5ac403895919c2a13aac599fa56b4362a92a953725fec8895c5bb3928aac2470db6bf94cceb52281b2c9a9a4d26c075f70fe6a120c932ddd17111d6141b7ba2663b55b1e60b7195777a1a54dc0f17f00b7e2e6fb1ade01cd3b7d98d08840e51a3985d39f6fbace6d', 'e': '0x1fd4b656fe65d679b4bd168d7ad11bcfaf9f126af9c65eb1f8a99752a1c5629199cb709e32c3ad397835122e83667f50c56cfd252fa8cc5bba37b3fc323cd24eef256605c7ca88666238e617ec5eb80cbf62ffd7245da2d2200044c015d977c3b960a622793f61810dc46f631aebba4166ab6af'}
        cle_public_r2 = {'nom' : 'Routeur 2', 'n': '0x5d24dc9b28a8cb3af3ff79147ae18bedb25a6398f9027a9f537cf19b6c409556eaf9c6cceb262b6c4704d50536829bbbdf820b8eeb7861929b242baba6e75f9f73c7593151995800feef75e2c451de1af3d23fc5416000de68ed3f2922b71d43123cf7ae08338458fc8aef0d55c090f5f21eddc432677a692d057033bc92e1e170e688be39b6a3e6eaf5b64dbad1e9620dfa05400356722c5ac403895919c2a13aac599fa56b4362a92a953725fec8895c5bb3928aac2470db6bf94cceb52281b2c9a9a4d26c075f70fe6a120c932ddd17111d6141b7ba2663b55b1e60b7195777a1a54dc0f17f00b7e2e6fb1ade01cd3b7d98d08840e51a3985d39f6fbace6d', 'e': '0x1fd4b656fe65d679b4bd168d7ad11bcfaf9f126af9c65eb1f8a99752a1c5629199cb709e32c3ad397835122e83667f50c56cfd252fa8cc5bba37b3fc323cd24eef256605c7ca88666238e617ec5eb80cbf62ffd7245da2d2200044c015d977c3b960a622793f61810dc46f631aebba4166ab6af'}
        cle_public_c1 = {'nom' : 'Client A', 'n': '0x5d24dc9b28a8cb3af3ff79147ae18bedb25a6398f9027a9f537cf19b6c409556eaf9c6cceb262b6c4704d50536829bbbdf820b8eeb7861929b242baba6e75f9f73c7593151995800feef75e2c451de1af3d23fc5416000de68ed3f2922b71d43123cf7ae08338458fc8aef0d55c090f5f21eddc432677a692d057033bc92e1e170e688be39b6a3e6eaf5b64dbad1e9620dfa05400356722c5ac403895919c2a13aac599fa56b4362a92a953725fec8895c5bb3928aac2470db6bf94cceb52281b2c9a9a4d26c075f70fe6a120c932ddd17111d6141b7ba2663b55b1e60b7195777a1a54dc0f17f00b7e2e6fb1ade01cd3b7d98d08840e51a3985d39f6fbace6d', 'e': '0x1fd4b656fe65d679b4bd168d7ad11bcfaf9f126af9c65eb1f8a99752a1c5629199cb709e32c3ad397835122e83667f50c56cfd252fa8cc5bba37b3fc323cd24eef256605c7ca88666238e617ec5eb80cbf62ffd7245da2d2200044c015d977c3b960a622793f61810dc46f631aebba4166ab6af'}
        cle_public_c2 = {'nom' : 'Client B', 'n': '0x5d24dc9b28a8cb3af3ff79147ae18bedb25a6398f9027a9f537cf19b6c409556eaf9c6cceb262b6c4704d50536829bbbdf820b8eeb7861929b242baba6e75f9f73c7593151995800feef75e2c451de1af3d23fc5416000de68ed3f2922b71d43123cf7ae08338458fc8aef0d55c090f5f21eddc432677a692d057033bc92e1e170e688be39b6a3e6eaf5b64dbad1e9620dfa05400356722c5ac403895919c2a13aac599fa56b4362a92a953725fec8895c5bb3928aac2470db6bf94cceb52281b2c9a9a4d26c075f70fe6a120c932ddd17111d6141b7ba2663b55b1e60b7195777a1a54dc0f17f00b7e2e6fb1ade01cd3b7d98d08840e51a3985d39f6fbace6d', 'e': '0x1fd4b656fe65d679b4bd168d7ad11bcfaf9f126af9c65eb1f8a99752a1c5629199cb709e32c3ad397835122e83667f50c56cfd252fa8cc5bba37b3fc323cd24eef256605c7ca88666238e617ec5eb80cbf62ffd7245da2d2200044c015d977c3b960a622793f61810dc46f631aebba4166ab6af'}
           
        liste_appareils = [cle_public_r1, cle_public_r2, cle_public_c1, cle_public_c2]
        """
        
        for appareil in self.appareils:
            self.liste_routeurs.emit(appareil)
    
    def run(self):
        """Méthodes"""
        self.liste_appareils()
        self.message_recus()
        

class RSAWorker(QObject):
    finished = pyqtSignal(dict, dict)  # signal émis quand le calcul est terminé

    def __init__(self, bits=2048):
        super().__init__()
        self.bits = bits

    def run(self):
        rsa = rt.RSA()
        rsa.cles(256)
        self.finished.emit(rsa.Kp, rsa.Km)

"""
class ServeurThread(QThread):
    def __init__(self, port):
        super().__init__()
        self.port = port

    def run(self):
        serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serveur.bind(('0.0.0.0', self.port))
        serveur.listen()

        while True:
            connexion, adresse = serveur.accept()
            # Lancer la gestion des clients dans un thread séparé
            thread = threading.Thread(
                target=gestion_clients,
                args=(connexion, adresse),
                daemon=True
            )
            thread.start()
"""

"""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qss)
    # RSA
    rsa = rt.RSA()
    rsa.cles(256)
    ma_kp = rsa.Kp
    ma_km = rsa.Km
    
    cle_public_r1 = {'nom' : 'Routeur 1', 'n': '0x5d24dc9b28a8cb3af3ff79147ae18bedb25a6398f9027a9f537cf19b6c409556eaf9c6cceb262b6c4704d50536829bbbdf820b8eeb7861929b242baba6e75f9f73c7593151995800feef75e2c451de1af3d23fc5416000de68ed3f2922b71d43123cf7ae08338458fc8aef0d55c090f5f21eddc432677a692d057033bc92e1e170e688be39b6a3e6eaf5b64dbad1e9620dfa05400356722c5ac403895919c2a13aac599fa56b4362a92a953725fec8895c5bb3928aac2470db6bf94cceb52281b2c9a9a4d26c075f70fe6a120c932ddd17111d6141b7ba2663b55b1e60b7195777a1a54dc0f17f00b7e2e6fb1ade01cd3b7d98d08840e51a3985d39f6fbace6d', 'e': '0x1fd4b656fe65d679b4bd168d7ad11bcfaf9f126af9c65eb1f8a99752a1c5629199cb709e32c3ad397835122e83667f50c56cfd252fa8cc5bba37b3fc323cd24eef256605c7ca88666238e617ec5eb80cbf62ffd7245da2d2200044c015d977c3b960a622793f61810dc46f631aebba4166ab6af'}
    cle_public_r2 = {'nom' : 'Routeur 2', 'n': '0x5d24dc9b28a8cb3af3ff79147ae18bedb25a6398f9027a9f537cf19b6c409556eaf9c6cceb262b6c4704d50536829bbbdf820b8eeb7861929b242baba6e75f9f73c7593151995800feef75e2c451de1af3d23fc5416000de68ed3f2922b71d43123cf7ae08338458fc8aef0d55c090f5f21eddc432677a692d057033bc92e1e170e688be39b6a3e6eaf5b64dbad1e9620dfa05400356722c5ac403895919c2a13aac599fa56b4362a92a953725fec8895c5bb3928aac2470db6bf94cceb52281b2c9a9a4d26c075f70fe6a120c932ddd17111d6141b7ba2663b55b1e60b7195777a1a54dc0f17f00b7e2e6fb1ade01cd3b7d98d08840e51a3985d39f6fbace6d', 'e': '0x1fd4b656fe65d679b4bd168d7ad11bcfaf9f126af9c65eb1f8a99752a1c5629199cb709e32c3ad397835122e83667f50c56cfd252fa8cc5bba37b3fc323cd24eef256605c7ca88666238e617ec5eb80cbf62ffd7245da2d2200044c015d977c3b960a622793f61810dc46f631aebba4166ab6af'}
    cle_public_c1 = {'nom' : 'Client A', 'n': '0x5d24dc9b28a8cb3af3ff79147ae18bedb25a6398f9027a9f537cf19b6c409556eaf9c6cceb262b6c4704d50536829bbbdf820b8eeb7861929b242baba6e75f9f73c7593151995800feef75e2c451de1af3d23fc5416000de68ed3f2922b71d43123cf7ae08338458fc8aef0d55c090f5f21eddc432677a692d057033bc92e1e170e688be39b6a3e6eaf5b64dbad1e9620dfa05400356722c5ac403895919c2a13aac599fa56b4362a92a953725fec8895c5bb3928aac2470db6bf94cceb52281b2c9a9a4d26c075f70fe6a120c932ddd17111d6141b7ba2663b55b1e60b7195777a1a54dc0f17f00b7e2e6fb1ade01cd3b7d98d08840e51a3985d39f6fbace6d', 'e': '0x1fd4b656fe65d679b4bd168d7ad11bcfaf9f126af9c65eb1f8a99752a1c5629199cb709e32c3ad397835122e83667f50c56cfd252fa8cc5bba37b3fc323cd24eef256605c7ca88666238e617ec5eb80cbf62ffd7245da2d2200044c015d977c3b960a622793f61810dc46f631aebba4166ab6af'}
    cle_public_c2 = {'nom' : 'Client B', 'n': '0x5d24dc9b28a8cb3af3ff79147ae18bedb25a6398f9027a9f537cf19b6c409556eaf9c6cceb262b6c4704d50536829bbbdf820b8eeb7861929b242baba6e75f9f73c7593151995800feef75e2c451de1af3d23fc5416000de68ed3f2922b71d43123cf7ae08338458fc8aef0d55c090f5f21eddc432677a692d057033bc92e1e170e688be39b6a3e6eaf5b64dbad1e9620dfa05400356722c5ac403895919c2a13aac599fa56b4362a92a953725fec8895c5bb3928aac2470db6bf94cceb52281b2c9a9a4d26c075f70fe6a120c932ddd17111d6141b7ba2663b55b1e60b7195777a1a54dc0f17f00b7e2e6fb1ade01cd3b7d98d08840e51a3985d39f6fbace6d', 'e': '0x1fd4b656fe65d679b4bd168d7ad11bcfaf9f126af9c65eb1f8a99752a1c5629199cb709e32c3ad397835122e83667f50c56cfd252fa8cc5bba37b3fc323cd24eef256605c7ca88666238e617ec5eb80cbf62ffd7245da2d2200044c015d977c3b960a622793f61810dc46f631aebba4166ab6af'}
           
    cles_publiques = [cle_public_r1, cle_public_r2, cle_public_c1, cle_public_c2]
    
    # Fenêtre client
    fenetre_client = Client("Client G", "126.46.51.6", 54310, ma_kp, ma_km)
    fenetre_client.showMaximized()
    # Thread client
    worker = ClientWorker("Client G", "126.46.51.6", 54310, ma_kp, ma_km)
    thread = QThread()
    worker.moveToThread(thread)
    # Réception des messages
    worker.message_recu.connect(fenetre_client.message_recu)
    # Fermeture du thread
    worker.message_recu.connect(thread.quit)
    worker.message_recu.connect(worker.deleteLater)
    thread.finished.connect(thread.deleteLater)
    # Début du thread
    thread.started.connect(worker.run)
    thread.start()
    
    # Fermeture application
    sys.exit(app.exec())
"""




