"""
ROTATOR v1

Plus d'informations sur https://github.com/theofefe22/sae302

2025 - Altech Industries - Tous droits réservés

"""

# BIBLIOTHEQUES IMPORTEES
import socket
import random as rd
from sympy import isprime as isp


# VARIABLES LOCALES
x25519 = ((2**255)-19)
fi = (1+(5**.5))/2
pi = rd._pi
e = rd._e
rds = rd.SystemRandom()
os = rd._os


# FONCTIONS COMMUNES
def nom() -> str:
    """Renvoie le nom de la machine"""
    return socket.gethostname()

def ip() -> str:
    """Renvoie l'adresse IPv4 de la machine"""
    return socket.gethostbyname(socket.gethostname())


# LISTE DE CLASSES
class A64:
    """
    Classe de l'alphabet 64
        
    Méthodes :
        alfa() : Choix de l'alphabet
        binalfa() : Conversion de l'alphabet sur 6 bits
        z64() : Conversion d'un entier vers base 64 0z
        z64_inverse() : Conversion d'un base 64 0z vers un entier
    """
    
    def alfa(self, numero_alphabet: int = None) -> str:
        """
        Renvoie un alphabet choisi
        
        Argument :
            numero_alphabet (int) : Numéro de l'alphabet choisi
           
        Renvoie :
            alfa (str) : Chaîne de caractères de l'alphabet choisi
        """
        # Caractéristique numéro alphabet
        if numero_alphabet == None:
            numero_alphabet = self.__x
        # Caractéristiques alphabets
        if numero_alphabet == 1:
            alfa = "kZf3TgRHDyAw2dXvMj7U0CcN Bl5QsI1oPpE8beLaKnVzYxWiOhJ6GqSrt4uF9m!"
        elif numero_alphabet == 2:
            alfa = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcd efghijk!lmnopqrstuvwxyz1234567890"
        elif numero_alphabet == 3:
            alfa = "ae7RdcPnrk2gWQDOUuFhM4KLptvz9XEG5ob1ICZNYi0A6x 8JlHTfsyjVmqwBS3!"
        elif numero_alphabet == 4:
            alfa = "dRuAWDrQJiHhL1FSg5a7ps0OfG36Eot8bBCk9PUcT4 qZj!NnYXzwMVmK2lIvexy"
        elif numero_alphabet == 5:
            alfa = "EACzHvjsSY0f5PMIJNGq246WtDao bdhrFgulZxcVKw39Q1LBT8O7UXRmi!ykpen"
        elif numero_alphabet == 6:
            alfa = "hSz2 cEaojei3ldqD0Oy67JH4Q8CYKBIfpRT!wbnmkvtL9NMVAsrg5ZFxuGPUWX1"
        elif numero_alphabet == 7:
            alfa = "t5BQyO098rb!PAEWdlpN6YXMks3quJ HoGURw1DxghfFcV2avmInTZK7zLSjCe4i"
        elif numero_alphabet == 8:
            alfa = "wcQIB7r281tDJXqOkLjbFug3GdHUy0KRS5oElVxPMTW!vmZNpn CfA96esYa4zih"
        elif numero_alphabet == 9:
            alfa = "xB5 mcEHquKJoLyOtTrRM8XQnli!kZFgf9Nh4a62pwGU70esVSC3DdWAPYIvj1bz"
        elif numero_alphabet == 10:
            alfa = "KkGYiq gTBVtXxJwCfZ7mQphb39Ooen!c1RNuUSjE2arlDPL08zI6yF4H5MWAsvd"
        else:
            raise ValueError("L'alphabet n'existe pas.")
        return alfa
    
    def binalfa(self, numero_alphabet: int = None) -> dict:
        """
        Conversion de l'alphabet choisi vers un dictionnaire avec le caractère associé à une valeur binaire sur 6 bits
        
        Argument :
            numero_alphabet (int) : Numéro de l'alphabet choisi
        
        Renvoie :
            binalfa (dict) : Dictionnaire de l'alphabet utilisé
        """
        # Caractéristiques numéro alphabet
        if numero_alphabet == None:
            numero_alphabet = self.__x
        if 0 < numero_alphabet < 11:
            binalfa = {lettre: format(i, '06b') for i, lettre in enumerate(self.alfa(numero_alphabet))}
        else:
            raise ValueError("L'alphabet n'existe pas.")
        return binalfa
    
    def z64(self, nombre: int = None, numero_alphabet: int = None) -> str:
        """
        Conversion d'entier vers z64
        
        Arguments :
            nombre (int) : Nombre à convertir
            numero_alphabet (int) : Numéro de l'alphabet à utiliser
        
        Renvoie :
            nombre_convertit (str) : Nombre convertit base 64, avec préfixe 0z
        """
        # Caractéristiques du nombre
        if nombre == None:
            nombre = rds.randint(123,8973218)
        elif not isinstance(nombre, int):
            raise ValueError("Le format n'est pas correcte, veuilez renseigner au format 'int'.")
        # Caractéristiques de l'alphabet à utiliser
        if numero_alphabet == None:
            numero_alphabet = 2
        elif not isinstance(numero_alphabet, int):
            raise ValueError("Le format n'est pas correcte, veuilez renseigner au format 'int'.")
        # Si le nombre vaut zéro
        if nombre == 0:
            return "0z" + alfa(numero_alphabet)[0]
        # Sinon
        symbol = []
        while nombre > 0:
            nombre, reste = divmod(nombre, 64)
            symbol.append(self.alfa(numero_alphabet)[reste])
        return "0z" + "".join(reversed(symbol))
    
    def z64_inverse(self, nombre_0z: str, alfabet: int = 2) -> int:
        """
        Conversion de z64 en entier
        
        Arguments :
            nombre (str) : Nombre base 0z à convertir
            alfabet (int) : Numéro de l'alphabet à utiliser
        
        Renvoie :
            nombre (int) : Entier déconvertit
        """
        # Caractéristiques nombre_0z
        if not isinstance(nombre_0z, str):
            raise ValueError("Le format n'est pas correcte, veuilez renseigner au format 'str'.")
        if not nombre_0z.startswith("0z"):
            raise ValueError("Le code doit être une chaîne commençant par '0z'.")
        # Variables
        nombre_0z = nombre_0z[2:]
        alfa = self.alfa(alfabet)
        nombre = 0
        # Programme principal
        for caractere in nombre_0z:
            if caractere not in alfa:
                raise ValueError(f"Le caractère '{caractere}' n'est pas dans l'alphabet.")
            valeur = alfa.index(caractere)
            nombre = nombre * 64 + valeur
        return nombre


class BDD:
    """
    Classe de la base de données (BDD)
    
    Arguments :
        adresse (str) : Adresse IP du serveur
        port (int) : Port de connexion au serveur
        
    Méthodes :
        inserer(table, ip, port, kp) : Insertion de données
        recuperer(table) : Récuperation de données
        fermer() : Fermeture de la connexion à la base de données
    """
    def __init__(self, hote, utilisateur, mdp, base):
        self.__bdd = mysql.connector.connect(host = hote, user = utilisateur, password = mdp)
        self.cursor = self.__bdd.cursor()
        self.__base = base
        
        try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.__base}")
            print(f"Base '{self.__base}' créée ou déjà existante.")
        except mysql.connector.Error as err:
            print("Erreur création base:", err)
        # Se connecter à la BDD créée
        self.cursor.execute(f"USE {self.__base}")

    @property
    def base(self) -> str:
        """Renvoie la base de données utilisé"""
        return self.__base
        
    def inserer(self, table: str, ip: str, port: int, kp: list) -> None:
        """
        Insertion de données
        
        Arguments :
            table (str) : Table à utiliser
            ip (str) : IP à insérer
            port (int) : Port à insérer
            kp (list) : Clé publique à insérer
        """
        n = kp[0]
        e = kp[1]
        sql = f"INSERT INTO {table} (ip, port, n, e) VALUES (%s, %s, %s, %s)"
        valeurs = (ip, port, n, e)
        self.cursor.execute(sql, valeurs)
        self.__bdd.commit()
        print(self.cursor.rowcount, f"lignes insérées dans la table {table}.")
        
    def recuperer(self, table: str) -> list:
        """
        Récuperation de données d'une table
        
        Arguments :
            table (str) : Table à utiliser
        
        Renvoie :
            liste (list) : Eléments de la table
        """
        sql = f"SELECT * FROM {table}"
        self.cursor.execute(sql)
        liste = self.cursor.fetchall()
        return liste
    
    def fermer(self) -> None:
        """Fermeture de la connexion à la base de données"""
        self.cursor.close()
        self.__bdd.close()


class Client:
    """
    Classe du connecteur client
    
    Arguments :
        adresse (str) : Adresse IP du serveur
        port (int) : Port de connexion au serveur
        
    Méthodes :
        connexion() : Connexion au serveur
        enoie(message) : Envoie d'un message au serveur
        recption() : Message reçu du serveur
        fin() : Fermeture de la connexion au serveur
    """
    def __init__(self, adresse: str = "127.0.0.1", port: int = 1200) -> None:
        """Initialisation de l'IP et du port du serveur"""
        self.srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__adr = adresse
        self.__port = port
        
    @property
    def adresse(self) -> str:
        """Renvoie l'adresse du serveur"""
        return self.__adr
    
    @adresse.setter
    def adresse(self, adresse: str) -> None:
        """Modifie l'adresse du serveur"""
        if isinstance(adresse, str):
            self.__adr = adresse
        else:
            raise ValueError("Le format n'est pas correcte.")
        
    @property
    def port(self) -> int:
        """Renvoie le port du serveur"""
        return self.__port
    
    @port.setter
    def port(self, port: int) -> None:
        """Modifie l'adresse du port"""
        if isinstance(port, int):
            self.__port = port
        else:
            raise ValueError("Le format n'est pas correcte.")
    
    def connexion(self, adresse: str = None, port: int = None) -> None:
        """
        Connexion au serveur
        
        Arguments :
            adresse (str) : Adresse IP du serveur
            port (int) : Port de connexion au serveur
        """
        if adresse is None:
            adresse = self.__adr
        if port is None:
            port = self.__port
        self.srv.connect((adresse, self.__port))
        print(f"Connexion au port {port} du serveur {adresse}")

    def envoie(self, message: str = None) -> None:
        """
        Envoie un message
        
        Argument :
            message : Message à envoyer
        """
        
        if isinstance(message, dict):
            message = ",".join(str(x) for x in message)
        
        message = message.encode()
        longueur = len(message)
        if longueur>1020:
            print(f"Message long de {len(message)}")
            front = longueur.to_bytes(4,"big")
            self.srv.sendall(front + message)
        else:
            self.srv.send(message)
        print(f"Message envoyé : {message}")
        
    def certificat(self, Kp):
        """
        r
        """
        
        
        
        taille_cle = 2048
        
        Kp = {"n" : 456, "e" : 853}
        
        n = Kp["n"]
        e = Kp["e"]
        ip = "15.46.46.8"
        
        parametres = n
        
        message = "".join(parametres) + b"ZOUZOUZOUBISOU" 
        
        
        #for i in 
        
        
        

    def reception(self) -> None:
        """Affiche un message reçu du serveur"""
        msg = self.srv.recv(1024)
        if not msg:
            print("Fin de la transmission")
            return None
        """
        elif msg[:2] == "LI":
            liste = msg.decode()
            liste = [int(x) for x in liste.split(",")]
        """
        print(f"Message reçu : {msg.decode()}")
        return msg.decode()

    def fin(self) -> None:
        """Met fin à la connexion au serveur"""
        self.srv.send("".encode())
        self.srv.close()
        print("Fin de la connexion")
    

class Serveur:
    """
    Classe du connecteur serveur
    
    Arguments :
        adresse (str) : Adresse IP du serveur
        port (int) : Port d'écoute
        
    Méthodes :
        ecoute() : Ecoute les clients
        message_client() : Affiche le message reçu
    """
    def __init__(self, port: int = 1200) -> None:
        """
        Initialisation de l'IP et du port du serveur
        """
        self.__adr = "0.0.0.0"
        self.__port = port
        self.srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.srv.bind((self.__adr, self.__port))
                break
            except OSError as e:
                if e.errno == 10048:
                    self.__port += 1
        print(f"Serveur en écoute sur le port {self.__port}")
        self.srv.listen(5)
        
    @property
    def adresse(self) -> str:
        """Renvoie l'adresse du serveur"""
        return self.__adr
        
    @property
    def port(self) -> int:
        """Renvoie le port du serveur"""
        return self.__port
    
    @port.setter
    def port(self, port: int) -> None:
        """Modifie l'adresse du port"""
        if isinstance(port, int):
            self.__port = port
        else:
            raise ValueError("Le format n'est pas correcte.")
            
    def ecoute(self) -> tuple:
        """
        Ecoute les clients qui veulent se connecter
        
        Renvoie :
            cs : Socket du client
            adr : Adresse du client
        """
        cs, adr = self.srv.accept()
        print(f"Une connexion a été acceptée depuis {adr}")
        cs.send("Bienvenue".encode())
        self.__cs = cs
        return cs, adr
    
    def message_client(self) -> str:
        """Affiche le message reçu"""
        clientsocket = self.__cs
        try:
            msg = clientsocket.recv(1024).decode()
        except ConnectionResetError:
            print("Le client a fermé la connexion brutalement")
        if not msg:
            print("Aucun message reçu pour le moment")
        print("Message reçu :", msg)
        return msg


class Maths:
    """
    Classe des fonctions mathématiques
        
    Méthodes :
        euclide_etendu(a, b) : Calcul les coefficients de Bézout tels que d = pgcd(a, b) = a*u + b*v
        gp(nombre_bits) : Génère un nombre premier de n (nombre_bits) bits
        pgcd(a, b) : Calcul le plus grand commun diviseur (PGCD) de deux nombres a et b
        premiers_entre_eux(a, b) : Vérifier si deux nombres a et b sont premiers entre eux
    """
    def __init__(self):
        pass
 
    @staticmethod
    def euclide_etendu(a: int, b: int) -> tuple:
        """
        Renvoie un tuple (d, u, v) tel que d = gcd(a, b) et au + bv = d
        
        Arguments :
            a (int) : Paramètre a
            b (int) : Paramètre b
        
        Renvoie :
            d, u, v (tuple) : Paramètres d, u et v
        """
        if b == 0:
            return (a, 1, 0)
        else:
            d, u1, v1 = Maths.euclide_etendu(b, a % b)
            u = v1
            v = u1 - (a // b) * v1
            return (d, u, v)
        
    @staticmethod
    def gp(nombre_bits: int) -> int:
        """
        Génère un nombre premier ayant n (nombre_bits) bits
        
        Argument :
            nombre_bits (int) : Longueur en bits du nombre généré
            
        Renvoie :
            nombre (int) : Nombre premier généré
        """
        nombre = 0
        while not isp(nombre): # Tant que le nombre n'est pas premier
            nombre = rds.getrandbits(nombre_bits) # Génère un nombre aléatoire de n bits
            nombre |= (1 << nombre_bits - 1) | 1  # S'assure que c'est bien un nombre de n bits et impair et ou logique avec nombre
        return nombre

    @staticmethod
    def pgcd(a: int, b: int) -> int:
        """
        Calcul le plus grand commun diviseur (PGCD)
        
        Arguments :
            a (int) : Coefficient a
            b (int) : Coefficient b
        
        Renvoie :
            a (int) : Plus grand diviseur commun
        """
        while b != 0:
            a, b = b, a % b
        return a
    
    @staticmethod
    def premiers_entre_eux(a: int, b: int) -> bool:
        """
        Calcul si deux nombres sont premiers entre eux
        
        Arguments :
            a (int) : Coefficient a
            b (int) : Coefficient b
        
        Renvoie :
            reponse (bool) : Vrai si les deux nombres sont premiers entre eux, sinon Faux
        """
        reponse = Maths.pgcd(a, b) == 1
        return reponse


class RSA:
    """
    Classe du chiffrement RSA
        
    Méthodes :
        cles() : Calcul les clés RSA
        chiff() : Chiffre un message, avec la clé publique du receveur
        dechiff() : Déchiffre un message
        torage(message) :
        detorage() :
        
    Renvoie :
        Kp0 (int) : Clé publique à transmettre
        Km (int) : Clé privée
    """    
    @property
    def delta(self) -> int:
        """Renvoie le delta de la clé privée"""
        return self.__delta
    
    @property
    def fichier_Km(self):
        """Renvoie l'emplacement du fichier de la clé privée"""
        return self.__fichier_km
    
    @property
    def Km(self) -> int:
        """Renvoie la clé privée"""
        return self.__cle_privee
    
    @property
    def fichier_Kp(self):
        """Renvoie l'emplacement du fichier de la clé privée"""
        return self.__fichier_kp
    
    @property
    def Kp(self) -> int:
        """Renvoie la clé publique"""
        return self.__cle_publique
        
    def cles(self, nombre_bits: int = 512) -> dict:
        """
        Renvoie les clés partagée et privée RSA
        
        Argument :
            nombre_bits (int) : Nombre de symboles hexadécimales de la clé RSA (1 symbole hexa = 4 bits)
        
        Renvoie :
            cle_privee (dict), cle_publique (dict) : La clé privée et la clé publique
        """
        # Caractéristiques nombre de bits
        if not isinstance(nombre_bits, int):
            raise ValueError("Le format n'est pas correcte, veuilez renseigner au format 'str'.")
        elif nombre_bits < 200:
            raise ValueError("Veuillez renseigner une valeur plus grande.")
        # Boucle de génération des paramètres p et q
        while True:
            p = Maths.gp(2 * nombre_bits)
            q = Maths.gp(2 * nombre_bits)
            self.__delta = abs(p - q)
            if self.__delta >= 2**100:
                break
        # Calcul de n et phi(n)
        n = p * q
        phi_n = (p - 1) * (q - 1)
        # Calcul du coefficient e
        e = phi_n
        while True:
            if Maths.premiers_entre_eux(phi_n, e) == False:
                e = Maths.gp(int(1.8 * nombre_bits))
            else:
                break
        # Calcul des coefficients tels que e*u + phi_n*v = pgcd(e,phi_n) = g = 1
        g, u, v = Maths.euclide_etendu(e, phi_n)
        # Calcul du coefficient d
        d = u % phi_n
        # Clé privée
        self.__cle_privee = {"p": hex(p), "q": hex(q), "d": hex(d)}
        # Clé publique        
        self.__cle_publique = {"n": hex(n), "e": hex(e)}
        # Longueur clés
        longueur = (len(hex(n)) - 2) * 4
        print(f"Des clés RSA de taille {longueur} bits ont été générées")
        return self.__cle_privee, self.__cle_publique
    
    def chiffrer(self, message: str = None, Kp1: dict = None) -> list:
        """
        Chiffre un message, en utilisant la clé publique d'un autre
        
        Arguments :
            message (str) : Message à déchiffrer
            Kp1 (dict) : Clé publique de l'autre
        
        Renvoie :
            chiffre (hex) : Message chiffré
        """
        # Caractéristiques du message à chiffrer
        if message == None:
            raise ValueError("Veuilez renseigner un message à chiffrer.")
        elif not isinstance(message, str):
            raise ValueError("Le format n'est pas correcte, veuilez renseigner au format 'str'.")
        # Caractéristiques de la clé publique de l'autre
        if Kp1 == None:
            raise ValueError("Veuillez renseigner la clé publique de l'autre")
        elif Kp1 == self.__cle_publique:
            raise ValueError("Veuillez renseigner la clé publique de l'autre, pas la vôtre")
        elif not isinstance(Kp1, dict):
            raise ValueError("Le format n'est pas correcte, veuilez renseigner au format 'dict'.")
        # Paramètres
        n1 = int(Kp1["n"], 16)
        e1 = int(Kp1["e"], 16)
        # Transformation du message en entier
        message_bytes = message.encode("utf-8")
        # Déchiffrement du message
        chiffre_bloc = []
        taille_bloc = (n1.bit_length() - 1) // 8
        for i in range(0, len(message_bytes), taille_bloc):
            bloc = message_bytes[i:i + taille_bloc]
            bloc_int = int.from_bytes(bloc, byteorder='big')
            chiffre = hex(pow(bloc_int, e1, n1))
            chiffre_bloc.append(chiffre)
        return chiffre_bloc

    def dechiffrer(self, message_a_dechiffrer: list = None) -> str:
        """
        Déchiffre un message, en utilisant ma clé privée
        
        Argument :
            message_a_dechiffrer (list) : Message à déchiffrer
        
        Renvoie :
            dechiffre (str) : Message déchiffré
        """
        # Caractéristiques du message à déchiffrer
        if message_a_dechiffrer == None:
            raise ValueError("Veuilez renseigner un message à déchiffrer.")
        elif not isinstance(message_a_dechiffrer, list):
            raise ValueError("Le format n'est pas correcte, veuilez renseigner au format 'list'.")
        # Caractéristiques de ma clé publique
        d0 = int(self.__cle_privee["d"], 16)
        n0 = int(self.__cle_privee["p"], 16) * int(self.__cle_privee["q"], 16)
        # Déchiffrage
        message_bytes = b""
        for bloc_chiffre in message_a_dechiffrer:
            bloc_int = pow(int(bloc_chiffre, 16), d0, n0)
            nb_octets = (bloc_int.bit_length() + 7) // 8
            message_bytes += bloc_int.to_bytes(nb_octets, byteorder='big')
        message = message_bytes.decode("utf-8")
        return message
    
    def hacher2(self, message: str = None, sel: bytes = None) -> dict:
        """
        Hache un message en utilisant SHA512
        
        Arguments :
            message (str) : Message à hacher
            sel (bytes) : Sel du haché
        
        Renvoie :
            digere, sel (dict)
        """
        msgb = bytes(message, "utf-8")
        # Caractéristiques du sel
        if sel == None:
            sel = rds.randbytes(16)
        elif len(sel) < 16:
            raise ValueError("Le sel n'est pas assez salé, veuilez renseigner un sel d'au moins 16 octects.")
        # Fonction principale
        sha512 = rd._sha512
        hachis = sha512(msgb + sel)
        digere = hachis.digest()
        return {"digere" : digere, "sel" : sel}
    
    def signer(self, message_a_signer: str = None) -> list:
        """
        Signe un message
        
        Arguments :
            message_a_signer (str) : Message à signer
        
        Renvoie :
            message_a_signer, hex(signe), sel (list) : Le message à signer, le message signé et le sel
        """
        # Caractéristiques du message à signer
        if isinstance(message_a_signer, list):
            message_a_signer = str(message_a_signer)
        # Caractéristiques de ma clé privée
        Km = self.__Km
        # Paramètres
        d0 = int(Km[2],16)
        n0 = int(Km[0],16)*int(Km[1],16)
        # Calcul du haché
        try:
            hache = self.hacher2(message_a_signer)
            sel = hache[1]
            hache = int.from_bytes(hache[0],"big")
        except:
            return("Le haché n'a pas pu être obtenu.")
        # Cryptage du haché
        signe = pow(hache, d0, n0)
        return {"message": message_a_signer, "signe": hex(signe), "sel": sel}
    
    def verifier(self, message_signe: str, methode_hache: int = 2, Kp1: dict = None) -> bool:
        """
        Vérifie la signature d'un message
        
        Arguments :
            message_signe (str) : Message à signer
            Kp1 (dict) : La clé publique de l'autre
        
        Renvoie :
            (bool) : Vrai si l'authentification est bonne, Faux sinon
        """
        # Caractéristiques clé publique de l'autre
        if Kp1 == None:
            Kp1 = self.__Kp1
        elif Kp1 == self.__Kp:
            raise ValueError("Veuillez renseigner la clé publique de votre correspondant.")
        # Variables
        message = message_signe[0]
        signe = int(message_signe[1],16)
        # Hacher le message reçu
        if methode_hache == 1:
            dessigne_prime = int(self.hacher1(message),16)
        elif methode_hache == 2:
            sel = message_signe[2]
            dessigne_prime = int.from_bytes(self.hacher2(message,sel)[0],"big")     
        print(dessigne_prime)
        # Décripter la signature
        n1 = int(Kp1[0],16)
        e1 = int(Kp1[1],16)
        print(signe)
        dessigne = pow(signe, e1, n1)
        print(dessigne)
        # Comparaison
        if dessigne == dessigne_prime:
            print("La signature est correcte !")
            return True
        else:
            print("La signature n'est pas bonne")
            return False
    
    def torage(self, message: str, passage_norm: tuple, liste_cles: list) -> list:
        """
        Mise en oignon d'un message
        
        Arguments :
            message (str) : Message à chiffrer
            passage_norm (tuple) : Ordre de passage des routeurs par lesquels le message va passer
            liste_cles (list) : Liste des clés de toutes les machines
        
        Renvoie :
            chiffre (list) : L'oignon chiffré
        """
        # Caractéristiques du message
        if message == None:
            raise ValueError("Veuilez renseigner un message à transmettre.")
        elif not isinstance(message, str):
            raise ValueError("Le format n'est pas correcte, veuilez renseigner au format 'str'.")
        # Caractéristiques de l'ordre de passage
        if passage_norm == None:
            raise ValueError("Veuilez renseigner l'ordre de passage.")
        elif not isinstance(passage_norm, tuple):
            raise ValueError("Le format n'est pas correcte, veuilez renseigner au format 'tuple'.")
        passage = tuple(reversed(passage_norm))
        # Caractéristiques de la liste des routeurs
        if liste_cles == None:
            raise ValueError("Veuilez renseigner la liste des routeurs.")
        elif not isinstance(liste_cles, list):
            raise ValueError("Le format n'est pas correcte, veuilez renseigner au format 'list'.")
        # Mise en ordre des clés
        cles_publiques_reordonnees = []
        for routeur in passage_norm:
            for cle in liste_cles:
                if cle['nom'] == routeur:
                    cles_publiques_reordonnees.append(cle)
                    break
        if len(cles_publiques_reordonnees) == 0:
            raise ValueError("Les noms ne correspondent pas aux valeurs des clés.")
        # Premier chiffrage pour destinataire final
        destinataire = cles_publiques_reordonnees[0]
        chiffre = self.chiffrer(message, cles_publiques_reordonnees[-1])
        # Chiffrage
        n = 0
        for i in range(len(passage_norm) - 2, -1, -1):
            chiffre = passage[n] + str(chiffre)
            n += 1
            chiffre = self.chiffrer(chiffre, cles_publiques_reordonnees[i])
        return chiffre, destinataire

    def detorage(self, message_chiffre: list) -> str:
        """
        Décompactage du message chiffré
        
        Argument :
            message_chiffre (list) : Message chiffré reçu
        
        Renvoie :
            destinataire (str), message_a_envoyer (list/str) : Destinataire du message, Message à renvoyer
        """
        # Déchiffrage
        dechiffre = self.dechiffrer(message_chiffre)
        # Identification du destinataire
        i = dechiffre.find('[')
        destinataire = dechiffre[:i]
        # Calcul du message à envoyer
        u = dechiffre[i:]
        message_a_envoyer = [x.strip().strip("'") for x in u[1:-1].split(",")]
        # Pour le dernier destinataire
        if message_a_envoyer == ['']:
            message_a_envoyer = destinataire
            destinataire = "Aucun"
        return destinataire, message_a_envoyer

    def sauvegarde_cles(self, nom_fichier: str, alfa: int, cle: int) -> None:
        """
        Sauvergarde les clés RSA dans un fichier .pem
        
        Arguments :
            nom_fichier (str) : Nom racine du fichier
            alfa (int) : Numéro de l'alphabet de cryptage choisi
            K (int) : Coordonnée x de la clé partagée ECDHE
        """
        # Création des fichiers
        self.__fichier_kp = f"{nom_fichier}_cle_publique.pem"
        print(f"Le fichier {self.__fichier_kp} a été crée.")
        self.__fichier_km = f"{nom_fichier}_cle_privee.pem"
        print(f"Le fichier {self.__fichier_km} a été crée.")
        # Enregistrement de la clé publique
        with open(self.__fichier_kp, "w") as f:
            for nom, parametre in self.__cle_publique.items():
                f.write(f"{parametre}\n")       
        # Enregistrement de la clé privée
        with open(self.__fichier_km, "wb") as g:
            for nom in ["p", "q", "d"]:
                parametre_int = int(self.__cle_privee[nom], 16)
                param_bytes = parametre_int.to_bytes((parametre_int.bit_length() + 7) // 8, "big")
                cle_bytes = (str(cle).encode("utf-8") * ((len(param_bytes) // len(str(cle).encode("utf-8"))) + 1))[:len(param_bytes)]
                param_chiffre_bytes = bytes(a ^ b for a, b in zip(param_bytes, cle_bytes))
                g.write(bytes(A64().z64(int.from_bytes(param_chiffre_bytes, "big"), alfa), "utf-8") + b"ZOUZOUZOUBISOU")
        print("Enregistrement des clés effectué avec succès.")
        
    def chargement_cles(self, nom_fichier: str, alfa: int, cle: int) -> dict:
        """
        Charge les clés RSA
        
        Arguments :
            nom_fichier (str) : Nom racine du fichier
            alfa (int) : Numéro de l'alphabet de cryptage choisi
            cle (int) : Coordonnée x de la clé partagée ECDHE
        
        Renvoie :
            Kp (dict), Km (dict) : Clé publique, clé privée
        """
        self.__fichier_kp = f"{nom_fichier}_cle_publique.pem"
        self.__fichier_km = f"{nom_fichier}_cle_privee.pem"
        # Chargement de la clé publique
        with open(self.__fichier_kp, "rb") as f:
            self.__cle_publique = f.read()
        # Chargement de la clé privée
        with open(self.__fichier_km, "rb") as g:
            self.__cle_privee = g.read()
        # Décodage clé publique
        cle_publique_sec = [x for x in self.__cle_publique.decode('utf-8').replace("\r", "").split("\n") if x]
        self.__cle_publique = dict(zip(["n", "e"], cle_publique_sec))
        # Décodage clé privée
        cle_privee_sec = [bloc for bloc in self.__cle_privee.decode('utf-8').split("ZOUZOUZOUBISOU") if bloc]
        self.__cle_privee = {}
        for nom, bloc in zip(["p", "q", "d"], cle_privee_sec):
            param_chiffre_int = A64().z64_inverse(bloc, alfa)
            param_chiffre_bytes = param_chiffre_int.to_bytes((param_chiffre_int.bit_length() + 7) // 8, "big")
            cle_bytes = (str(cle).encode("utf-8") * ((len(param_chiffre_bytes) // len(str(cle).encode("utf-8"))) + 1))[:len(param_chiffre_bytes)]
            param_bytes = bytes(a ^ b for a, b in zip(param_chiffre_bytes, cle_bytes))
            self.__cle_privee[nom] = hex(int.from_bytes(param_bytes, "big"))
        return self.__cle_publique, self.__cle_privee


# CREDITS
print("Merci d'utiliser ROTATOR")


# BOUCLE DE TESTS
if __name__ == "__main__":
    print("Tests de fonctionnement")
    
    # Classes des tests
    a = A64()
    h = RSA()
    h.cles(512) # longueur clé env = 512 * 4 = 2048 bits
    
    
    