"""
ROTATOR v1

Plus d'informations sur https://github.com/theofefe22/sae302

2025 - Altech Industries - Tous droits réservés

"""
# BIBLIOTHEQUES
import socket
import random as rd
from sympy import isprime as isp
import __logo
import __gui as gui
import __secp256r1 as secp
import mysql.connector


# VARIABLES LOCALES
x25519 = ((2**255)-19)
fi = (1+(5**.5))/2
pi = rd._pi
e = rd._e
rds = rd.SystemRandom()
os = rd._os


# FONCTIONS COMMUNES
def nom():
    """Renvoie le nom de la machine"""
    return socket.gethostname()

def ip():
    """Renvoie l'adresse IPv4 de la machine"""
    return socket.gethostbyname(socket.gethostname())


# LISTE DE CLASSES
class A64:
    """
    Classe de l'alphabet 64
    
    Attributs:
        numero_alphabet (int) : Numéro de l'alphabet
        nombre (int) : Nombre à coder
        
    Méthodes:
        alfa() : Choix de l'alphabet
        binalfa() : Conversion de l'alphabet sur 6 bits
    """
    def __init__(self, numero_alphabet: int = 2, nombre: int = None) -> None:
        self.__x = numero_alphabet
        self.__nb = nombre
        
    @property
    def x(self) -> int:
        """Renvoie le numéro de l'alphabet"""
        return self.__x
    
    @x.setter
    def x(self, x: int) -> None:
        """Modifie le numéro de l'alphabet"""
        if isinstance(x, int):
            self.__x = x
        else:
            raise ValueError("Le format n'est pas correcte.")
        
    @property
    def nb(self) -> int:
        """?"""
        return self.__nb
    
    @nb.setter
    def nb(self, nb: int) -> None:
        """Modifie ?"""
        if isinstance(nb, int):
            self.__nb = nb
        else:
            raise ValueError("Le format n'est pas correcte.")
    
    def alfa(self, x: int = None):
        """Renvoie un alphabet choisi"""
        if x == None:
            x = self.__x
        if x == 1:
            alfa = "kZf3TgRHDyAw2dXvMj7U0CcN Bl5QsI1oPpE8beLaKnVzYxWiOhJ6GqSrt4uF9m!"
        elif x == 2:
            alfa = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcd efghijk!lmnopqrstuvwxyz1234567890"
        elif x == 3:
            alfa = "ae7RdcPnrk2gWQDOUuFhM4KLptvz9XEG5ob1ICZNYi0A6x 8JlHTfsyjVmqwBS3!"
        elif x == 4:
            alfa = "dRuAWDrQJiHhL1FSg5a7ps0OfG36Eot8bBCk9PUcT4 qZj!NnYXzwMVmK2lIvexy"
        elif x == 5:
            alfa = "EACzHvjsSY0f5PMIJNGq246WtDao bdhrFgulZxcVKw39Q1LBT8O7UXRmi!ykpen"
        elif x == 6:
            alfa = "hSz2 cEaojei3ldqD0Oy67JH4Q8CYKBIfpRT!wbnmkvtL9NMVAsrg5ZFxuGPUWX1"
        elif x == 7:
            alfa = "t5BQyO098rb!PAEWdlpN6YXMks3quJ HoGURw1DxghfFcV2avmInTZK7zLSjCe4i"
        elif x == 8:
            alfa = "wcQIB7r281tDJXqOkLjbFug3GdHUy0KRS5oElVxPMTW!vmZNpn CfA96esYa4zih"
        elif x == 9:
            alfa = "xB5 mcEHquKJoLyOtTrRM8XQnli!kZFgf9Nh4a62pwGU70esVSC3DdWAPYIvj1bz"
        elif x == 10:
            alfa = "KkGYiq gTBVtXxJwCfZ7mQphb39Ooen!c1RNuUSjE2arlDPL08zI6yF4H5MWAsvd"
        else:
            raise ValueError("L'alphabet n'existe pas.")
        return alfa
    
    def binalfa(self, x: int = None):
        if x == None:
            x = self.__x
        if x < 5:
            binalfa = {lettre: format(i, '06b') for i, lettre in enumerate(self.alfa(x))}
        else:
            raise ValueError("L'alphabet n'existe pas.")
        return binalfa
    
    def z64(self, nombre: int = None, alfabet: int = None):
        # Caractéristiques du nombre
        if nombre == None:
            nombre = rds.randint(123,8973218)
        elif not isinstance(nombre, int):
            raise ValueError("Le format n'est pas correcte, veuilez renseigner au format 'int'.")
        # Caractéristiques de l'alfabet à utiliser
        if alfabet == None:
            alfabet = 2
        elif not isinstance(message, int):
            raise ValueError("Le format n'est pas correcte, veuilez renseigner au format 'int'.")
        # Si le nombre vaut zéro
        if nombre == 0:
            return "0z" + alfa(2)[0]
        # Sinon
        symbol = []
        while nombre > 0:
            nombre, reste = divmod(nombre, 64)
            symbol.append(self.alfa(2)[reste])
        return "0z" + "".join(reversed(symbol))


class BDD:
    """
    Classe de la base de données (BDD)
    
    Attributs:
        adresse (str) : Adresse IP du serveur
        port (int) : Port de connexion au serveur
        
    Méthodes:
        connexion() : Connexion au serveur
        enoie(message) : Envoie d'un message au serveur
        recption() : Message reçu du serveur
        fin() : Fermeture de la connexion au serveur
    """
    def __init__(self, hote, utilisateur, mdp, bdd):
        self.__bdd = mysql.connector.connect(host=hote, user=utilisateur, password=mdp, database=bdd)
        self.cursor = self.__bdd.cursor()
    
    def commit(self):
        self.__bdd.commit()
        
    def insert(self, nom, ip, port, kp):
        n = kp[0]
        e = kp[1]
        sql = "INSERT INTO Routeurs2 (nom, ip, port, n, e) VALUES (%s, %s, %s, %s, %s)"
        valeurs = [(nom, ip, port, n, e)]
        self.cursor.executemany(sql, valeurs)
        self.commit()
        print(self.cursor.rowcount, "lignes insérées.")
        self.cursor.close()
    
    def fermer(self):
        self.__bdd.close()


class Client:
    """
    Classe du connecteur client
    
    Attributs:
        adresse (str) : Adresse IP du serveur
        port (int) : Port de connexion au serveur
        
    Méthodes:
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
        
        Arguments:
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
        
        Argument:
            message : Message à envoyer
        """
        
        if isinstance(message, list):
            message = ",".join(str(x) for x in message) #"LI" + 
        #elif isinstance(message, str):
            #self.srv.send(message.encode())
        
        message = message.encode()
        longueur = len(message)
        if longueur>1020:
            print(f"Message long de {len(message)}")
            front = longueur.to_bytes(4,"big")
        
        self.srv.sendall(front + message)
        #sock.sendall(header + data)
        #self.srv.send(message)
        print(f"Message envoyé : {message}")

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
        return msg

    def fin(self) -> None:
        """Met fin à la connexion au serveur"""
        self.srv.send("".encode())
        self.srv.close()
        print("Fin de la connexion")
    

class Serveur:
    """
    Classe du connecteur serveur
    
    Attributs:
        adresse (str) : Adresse IP du serveur
        port (int) : Port d'écoute
        
    Méthodes:
        ecoute() : Ecoute les clients
        message_client() : Affiche le message reçu
    """
    def __init__(self, port: int = 1200) -> None:
        """Initialisation de l'IP et du port du serveur"""
        self.__adr = "0.0.0.0"
        self.__port = port
        self.srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srv.bind((adresse, port))
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
        """Ecoute les clients qui veulent se connecter"""
        cs, adr = self.srv.accept()
        print(f"Une connexion a été acceptée depuis {adr}")
        cs.send("Bienvenue".encode())
        self.__cs = cs
        return cs, adr
    
    def message_client(self) -> bytes:
        """Affiche le message reçu"""
        clientsocket = self.__cs
        msg = clientsocket.recv(1024).decode()
        if not msg:
            print("Fin de la transmission")
            clientsocket.close()
            return None
        print("Message reçu :", msg)
        return msg


class Maths:
    """
    Classe des fonctions mathématiques
        
    Méthodes:
        euclide_etendu(a, b) : Calcul les coefficients de Bézout tels que d = pgcd(a, b) = a*u + b*v
        gp(nombre_bits) : Génère un nombre premier de n (nombre_bits) bits
        pgcd(a, b) : Calcul le plus grand commun diviseur (PGCD) de deux nombres a et b
        premiers_entre_eux(a, b) : Vérifier si deux nombres a et b sont premiers entre eux
    """
    def __init__(self):
        pass
 
    @staticmethod
    def euclide_etendu(a, b):
        """Renvoie un tuple (d, u, v) tel que d = gcd(a, b) et au + bv = d"""
        if b == 0:
            return (a, 1, 0)
        else:
            d, u1, v1 = Maths.euclide_etendu(b, a % b)
            u = v1
            v = u1 - (a // b) * v1
            return (d, u, v)
        
    @staticmethod
    def gp(nombre_bits):
        """Génère un nombre premier ayant n (nombre_bits) bits"""
        nombre = 0
        while not isp(nombre): # Tant que le nombre n'est pas premier
            nombre = rds.getrandbits(nombre_bits) # Génère un nombre aléatoire de n bits
            nombre |= (1 << nombre_bits - 1) | 1  # S'assure que c'est bien un nombre de n bits et impair et ou logique avec nombre
        return nombre
    
    """
    @staticmethod
    def matrice(a: int, b: int) -> int:
        while b != 0:
            a, b = b, a % b
        return a
    """

    @staticmethod
    def pgcd(a: int, b: int) -> int:
        """
        Calcul le plus grand commun diviseur (PGCD)
        
        Arguments:
            a (int) : Coefficient a
            b (int) : Coefficient b
        """
        while b != 0:
            a, b = b, a % b
        return a
    
    @staticmethod
    def premiers_entre_eux(a: int, b: int) -> bool:
        """
        Calcul si deux nombres sont premiers entre eux
        
        Arguments:
            a (int) : Coefficient a
            b (int) : Coefficient b
        """
        return Maths.pgcd(a, b) == 1


class DH:
    """
    Classe des clés de Diffie-Hellman
    
    Attributs:
        p (int) : Paramètre publique, nombre premier
        g (int) : Paramètre publique, avec g < 1
        Kp1 (int) : Clé publique reçue
        
    Méthodes:
        connexion() : Connexion au serveur
        enoie(message) : Envoie d'un message au serveur
        recption() : Message reçu du serveur
        fin() : Fermeture de la connexion au serveur
        
    Renvoie:
        Kp0 (int) : Clé publique à transmettre
        Km (int) : Clé privée
        K (int) : Clé partagée
    """
    def __init__(self, p: int = x25519, g: int = None, Kp1: int = None) -> None:
        self.__p = p
        self.__g = g
        self.__Kp1 = Kp1
        
    @property
    def Kp0(self) -> int:
        """Renvoie la clé publique à transmettre"""
        return self.__Kp0
    
    @property
    def Kp1(self) -> int:
        """Renvoie la clé publique reçue"""
        return self.__Kp1
    
    @Kp1.setter
    def Kp1(self, Kp1: int):
        """Modifie la clé publique reçue"""
        if isinstance(Kp1, int):
            self.__Kp1 = Kp1
        else:
            raise ValueError("Le format n'est pas correcte.")
        
    @property
    def K(self) -> int:
        """Renvoie la clé partagée"""
        return self.__K
        
    def cles(self) -> int:
        """Calcule les clés de Diffie-Hellman"""
        p = self.__p
        # Si p = x25519 alors la longueur est de 77 caractères
        g = self.__g
        # Détermine la clé privée, de taille inférieur ou égale à p
        Km = rds.randint(0, p-1)
        self.__Km = Km
        # Calcul la clé publique, de taille inférieur ou égale à p
        Kp0 = pow(g, Km, p)
        self.__Kp0 = Kp0
        return [Kp0, Km]
        
    def secret(self) -> int:
        """Détermine la clé partagée"""
        Kp1 = self.__Kp1
        Km = self.__Km
        p = self.__p
        K = pow(Kp1, Km, p)
        self.__K = K
        return K


class RSA:
    """
    Classe des clés de RSA
    
    Attributs:
        p (int) : Paramètre publique, nombre premier
        g (int) : Paramètre publique, avec g > 1
        Kp1 (int) : Clé publique reçue
        
    Méthodes:
        cles() : Calcul les clés
        chiff() : Chiffre un message
        dechiff() : Déchiffre un message
        
    Renvoie:
        Kp0 (int) : Clé publique à transmettre
        Km (int) : Clé privée
        K (int) : Clé partagée
    """
    def __init__(self, message_a_chiffrer: str = "Hell", message_a_dechiffrer: int = None, Kp1: list = None) -> None:
        self.__m0 = message_a_chiffrer
        self.__c1 = message_a_dechiffrer
        self.__Kp1 = Kp1
        self.__fichier_km = ""
        
    @property
    def c0(self) -> int:
        """Renvoie le mot chiffré par moi et codé sur un entier"""
        return self.__c0
    
    @property
    def m0(self) -> int:
        """Renvoie le mot à envoyer"""
        return self.__m0
    
    @m0.setter
    def m0(self, m0: str):
        """Modifie le mot à envoyer"""
        if isinstance(m0, str):
            self.__m0 = m0
        else:
            raise ValueError("Le format n'est pas correcte.")
    
    @property
    def c1(self) -> int:
        """Renvoie le mot chiffré par l'autre et codé sur un entier"""
        return self.__c1
    
    @c1.setter
    def c1(self, c1: int):
        """Modifie le mot chiffré par l'autre et codé sur un entier"""
        if isinstance(c1, int):
            self.__c1 = c1
        else:
            raise ValueError("Le format n'est pas correcte.")
    
    @property
    def m1(self) -> int:
        """Renvoie le mot reçu déchiffré"""
        return self.__m1
    
    @property
    def delta(self) -> int:
        """Renvoie le mot reçu déchiffré"""
        return self.__delta
    
    @property
    def fichier_km(self):
        """Renvoie l'emplacement du fichier de la clé privée"""
        return self.__fichier_km
    
    @property
    def Km(self) -> int:
        """Renvoie la clé privée"""
        return self.__Km
    
    @property
    def fichier_kp(self):
        """Renvoie l'emplacement du fichier de la clé privée"""
        return self.__fichier_kp
    
    @property
    def Kp(self) -> int:
        """Renvoie la clé publique"""
        return self.__Kp
    
    @property
    def Kp1(self) -> int:
        """Renvoie la clé publique reçue"""
        return self.__Kp1
    
    @Kp1.setter
    def Kp1(self, Kp1: int):
        """Modifie la clé publique reçue"""
        if isinstance(Kp1, int):
            self.__Kp1 = Kp1
        else:
            raise ValueError("Le format n'est pas correcte.")
    
    @property
    def n(self) -> int:
        """Renvoie la clé partagée"""
        return self.__n
        
    def cles(self, nombre_bits):
        """Renvoie les clés partagée et privée RSA"""
        nb = nombre_bits
        if nb < 200:
            raise ValueError("Veuillez renseigner une valeur plus grande.")
        p = Maths.gp(3*nb)
        q = Maths.gp(nb)
        delta = abs(p-q)
        self.__delta = delta
        n = p*q
        phi_n = (p-1)*(q-1)
        e = phi_n
        # Calcul du coefficient e
        while True:
            if Maths.premiers_entre_eux(phi_n, e) == False:
                e = Maths.gp(int(1.8*nb))
            else:
                break
        # Calcul des coefficients tels que e*u + phi_n*v = pgcd(e,phi_n) = g = 1
        g, u, v = Maths.euclide_etendu(e, phi_n)
        # Calcul du coefficient d
        d = u%phi_n
        # Clé privée
        Km = [hex(p), hex(q), hex(d)]
        self.__Km = Km
        # Clé publique
        Kp = [hex(n), hex(e)]
        self.__Kp = Kp
        print(f"Des clés RSA de taille {3*nombre_bits} bits ont été générées")
        return [Kp, Km]
    
    def chiff(self, message: str = None, Kp1: list = None):
        """
        Chiffre un message, en utilisant la clé publique d'un autre
        
        Arguments:
            message (str) : Message à déchiffrer
            Kp1 (list) : Clé publique de l'autre
        """
        # Caractéristiques du message à chiffrer
        if message == None:
            message = self.__m0
        elif not isinstance(message, str):
            raise ValueError("Le format n'est pas correcte, veuilez renseigner au format 'str'.")
        self.__m0 = message
        # Caractéristiques de la clé publique de l'autre
        if Kp1 == None:
            raise ValueError("Veuillez renseigner la clé publique de l'autre")
        elif Kp1 == self.__Kp:
            raise ValueError("Veuillez renseigner la clé publique de l'autre, pas la vôtre")
        elif not isinstance(Kp1, list):
            raise ValueError("Le format n'est pas correcte, veuilez renseigner au format 'list'.")
        # Transformation du message en entier
        m0 = int.from_bytes(message.encode(), byteorder='big')
        if m0 >= self.__n:
            raise ValueError(f"Le message est trop grand pour ce module RSA. Message = {hex(m0)} > {hex(self.__n)}")
        # Calcul du message chiffré
        n1 = int(Kp1[0],16)
        e1 = int(Kp1[1],16)
        c0 = hex(pow(m0, e1, n1))
        self.__c0 = c0
        return c0

    def dechiff(self, message_a_dechiffrer: int = None):
        """
        Déchiffre un message, en utilisant ma clé privée
        
        Argument:
            message_a_dechiffrer (int) : Message à déchiffrer
        """
        # Caractéristiques du message à déchiffrer
        c1 = int(message_a_dechiffrer, 16)
        if c1 == None:
            c1 = self.__c1
        elif not isinstance(c1, int):
            raise ValueError("Le format n'est pas correcte, veuilez renseigner au format 'int'.")
        # Caractéristiques de ma clé publique
        Km = self.__Km
        d0 = int(Km[2],16)
        n0 = int(Km[0],16)*int(Km[1],16)
        m1 = pow(c1, d0, n0)
        m1 = m1.to_bytes((m1.bit_length() + 7)//8, 'big').decode()
        return m1
    
    def hacher1(self, message: str) -> hex:
        """
        Hache un message
        
        Argument:
            message (str) : Message à hacher
        """
        valeur_hachage = 5381
        for caractere in message:
            valeur_hachage = ((valeur_hachage << 5) + valeur_hachage) + ord(caractere)
            valeur_hachage &= 0xFFFFFFFFFFFFFFFF
        return hex(valeur_hachage)
    
    def hacher2(self, message: str = None, sel: bytes = None):
        """
        Hache un message en utilisant SHA512
        
        Argument:
            message (str) : Message à hacher
            sel (bytes) : Sel du haché
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
        return [digere,sel]
    
    def signer(self, message_a_signer: str = None) -> list:
        """
        Signe un message
        
        Arguments:
            message_a_signer (str) : Message à signer
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
            hache = self.hacher1(message_a_signer)
            print("La haché a été obtenu à partir d'une fonction de hachage secondaire.")
            hache = int(hache,16)
            sel = 0
        # Cryptage du haché
        signe = pow(hache, d0, n0)
        return [message_a_signer, hex(signe), sel]
    
    def verifier(self, message_signe: str, methode_hache: int = 2, Kp1: list = None):
        """
        Vérifie la signature d'un message
        
        Arguments:
            message_signe (str) : Message à signer
            Kp1 (list) : La clé publique de l'autre
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


    def sauvegarde_cles(self):
        # Création des fichiers
        nom_fichier = os.path.splitext(os.path.basename(__file__))[0]
        self.__fichier_kp = f"{nom_fichier}_cle_publique.pem"
        print(f"Le fichier {self.__fichier_kp} a été crée.")
        self.__fichier_km = f"{nom_fichier}_cle_privee.pem"
        print(f"Le fichier {self.__fichier_km} a été crée.")
        # Enregistrement de la clé publique
        with open(self.__fichier_kp, "w") as f:
            for item in self.__Kp:
                f.write(f"{item}\n")
        # Enregistrement de la clé privée
        with open(self.__fichier_km, "w") as g:
            for item in self.__Km:
                g.write(f"{item}\n")
        print("Enregistrement des clés effectué avec succès.")
            
    def chargement_cles(self):
        """
        Chargement des clés
        
        Renvoie:
            Kp (tuple) : Clé publique
        """
        nom_fichier = os.path.splitext(os.path.basename(__file__))[0]
        self.__fichier_kp = f"{nom_fichier}_cle_publique.pem"
        self.__fichier_km = f"{nom_fichier}_cle_privee.pem"
        # Chargement de la clé publique
        with open(self.__fichier_kp, "rb") as f:
            Kp = f.read()
        # Chargement de la clé privée
        with open(self.__fichier_km, "rb") as g:
            Km = g.read()
        return Kp, Km


class ECDHE:
    """
    Classe du chiffrement ECDHE (Diffie Hellman Ephémère à Courbe Elliptique) sur la courbe Scep256r1
         
    Méthodes:
        cle_privee() : Calcul de la clé privée
        cle_publique() : Calcul de la clé publique
        cle_partagee() : Calcul de la clé partagée
        signer(message) : Signe un message
        flux_sha512() : Génère un flux pseudo-aléatoire
        chiffrer(message) : Chiffre / déchiffre un message
    """
    def __init__(self):
        self.__Gx = secp.Gx
        self.__Gy = secp.Gy
    
    @property
    def G(self) -> list:
        """Renvoie le point générateur G"""
        self.__G = [hex(self.__Gx), hex(self.__Gy)]
        return self.__G
    
    @property
    def Km(self) -> int:
        """Renvoie ma clé privée"""
        return self.__Km
    
    @property
    def Kp(self) -> tuple:
        """Renvoie la clé publique"""
        return self.__Kp
    
    @property
    def K(self) -> tuple:
        """Renvoie la clé partagée"""
        return self.__K
    
    def cle_privee(self) -> int:
        """
        Calcul de la clé privée
        
        Renvoie:
            Km (int) : Clé privée
        """
        self.__Km = rds.randint(1, secp.n-1)
        return self.__Km
    
    def cle_publique(self) -> tuple:
        """
        Calcul de la clé publique
        
        Renvoie:
            Kp (tuple) : Clé publique
        """
        self.__Kp = secp.montgomery_ladder(self.__Km, self.__Gx, self.__Gy)
        return self.__Kp
    
    def cle_partagee(self, Kp1: list) -> tuple:
        """
        Calcul de la clé partagée
        
        Attribut:
            Kp1 (tuple) : Clé partagée de l'interlocuteur
        """
        self.__K = secp.montgomery_ladder(self.__Km, Kp1[0], Kp1[1])
        return self.__K
    
    def signer(self, message: bytes) -> hex:
        """
        Signe un message
        
        Attribut:
            message (bytes) : Message à chiffrer ou déchiffrer
            
        Renvoie:
            signe (hex) : Message signé
        """
        Kx = self.__K[0]
        key = Kx.to_bytes((Kx.bit_length() + 7) // 8, byteorder='big')
        bloc = 128
        
        # Étape 1 : Ajuster la clé
        if len(key) > bloc:
            key = rd._sha512(key).digest()  # hacher si trop long
        if len(key) < bloc:
            key = key.ljust(bloc, b'\x00')  # compléter avec des zéros
        
        # Étape 2 : Créer ipad et opad
        ipad = bytes((x ^ 0x36) for x in key)
        opad = bytes((x ^ 0x5c) for x in key)
    
        # Étape 3 : Calcul HMAC
        inner_hash = rd._sha512(ipad + message).digest()
        hmac_result = rd._sha512(opad + inner_hash).hexdigest()
        return hmac_result

    def chiffrer(self, message):
        """
        Chiffre un message
        
        Attribut:
            message (bytes/str) : message à chiffrer (str) ou à déchiffrer (bytes)
        
        Renvoie:
            chiffre (bytes/str) : message chiffré (bytes) ou déchiffré (str)
        """
        # Caractéristiques du message
        drapeau = 0
        if isinstance(message, str):
            message = message.encode("utf-8")
            drapeau = 1
        elif isinstance(message, bytes):
            message = message
            drapeau = 2
        else:
            raise ValueError("Le format n'est pas correcte, veuillez renseigner un str ou un bytes.")
        cleX = self.__K[0]
        nombre = (cleX.bit_length() + 7) // 8
        cle = cleX.to_bytes(nombre, byteorder='big')    
        longueur = len(message)
        # Balance XOR
        flux = b""
        compteur = 0
        while len(flux) < longueur:
            # Concatène la clé avec un compteur pour produire des blocs uniques
            block = rd._sha512(cle + compteur.to_bytes(8, 'big')).digest()
            flux += block
            compteur += 1
        # Chiffré
        chiffre = flux[:longueur]     
        #resultat = bytes([m ^ k for m, k in zip(message, chiffre)])
        
        if drapeau == 1:
            resultat = bytes([m ^ k for m, k in zip(message, chiffre)])
        elif drapeau == 2:
            resultat = bytes([m ^ k for m, k in zip(message, chiffre)]).decode("utf-8")
        
        return resultat


print("Merci d'utiliser ROTATOR")

if __name__ == "__main__":
    print("Tests de fonctionnement")
    kp = rd.randint(0, x25519-1)
    k = DH(x25519,999,kp)
    # Le module os est intégré dans random
    os.path.exists('rotator.py')
    h = RSA()
    
    
    # Génère des clés de 3 x 683 hex = 2049 bits
    if not os.path.exists(f"{os.path.splitext(os.path.basename(__file__))[0]}_cle_publique.pem"):
        h.cles(683)
        h.sauvegarde_cles()
    

    ma_cle_publique, ma_cle_privee = h.chargement_cles()
    
    Kp = [x for x in ma_cle_publique.decode().replace("\r", "").split("\n") if x]
    Km = [x for x in ma_cle_publique.decode().replace("\r", "").split("\n") if x]
    
    """
    h.Km = Km
    h.Kp = Kp
    """
    
    
    a = A64()
    
    liste_alfa = rd.sample(range(64), 64)
    
    
    
   # Appuyer sur ctrl + T
    
    










