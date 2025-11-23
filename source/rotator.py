# BIBLIOTHEQUES
import socket
import random as rd
from sympy import isprime as isp

# VARIABLES LOCALES
x25519 = ((2**255)-19)

# FONCTIONS COMMUNES
def nom():
    """Renvoie le nom de la machine"""
    return socket.gethostname()

def ip():
    """Renvoie l'adresse IPv4 de la machine"""
    return socket.gethostbyname(socket.gethostname())

# LISTE DE CLASSES
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
    def __init__(self, adresse: str="127.0.0.1", port: int=1200) -> None:
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
    
    def connexion(self, adresse=None, port=None) -> None:
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

    def envoie(self, message) -> None:
        """
        Envoie un message
        
        Argument:
            message : Message à envoyer
        """
        self.srv.send(message.encode())
        print("Message envoyé")

    def reception(self) -> None:
        """Affiche un message reçu du serveur"""
        msg = srv.recv(1024)
        print(f"Message reçu : {msg.decode()}")

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
    """
    def __init__(self, adresse: str="localhost", port: int=1200) -> None:
        """Initialisation de l'IP et du port du serveur"""
        self.__adr = adresse
        self.__port = port
        self.srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srv.bind((adresse, port))
        self.srv.listen(5)
        
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
            
    def ecoute(self) -> tuple:
        """Ecoute les clients qui veulent se connecter"""
        cs, adr = self.srv.accept()
        print(f"Une connexion a été acceptée depuis {adr}")
        cs.send("Bienvenue".encode())
        return cs, adr
    
    def message_client(self, clientsocket) -> bytes:
        """Affiche le message reçu"""
        msg = clientsocket.recv(1024)
        if not msg:
            print("Fin de la transmission")
            return None
        print("Message reçu :", msg.decode())
        return msg


class Maths:
    def __init__(self):
        pass
    
    @staticmethod
    def pgcd(a: int, b: int) -> int:
        """Calcul le plus grand commun diviseur (PGCD)"""
        while b != 0:
            a, b = b, a % b
        return a
    
    @staticmethod
    def premiers_entre_eux(a: int, b: int) -> bool:
        """Calcul si deux nombres sont premiers entre eux"""
        return self.pgcd(a, b) == 1
    
    @staticmethod
    def gp(nombre_bits):
        """Génère un nombre premier ayant n (nombre_bits) bits"""
        nombre = 0
        while not isp(nombre): # Tant que le nombre n'est pas premier
            nombre = rd.getrandbits(nombre_bits) # Génère un nombre aléatoire de n bits
            nombre |= (1 << nombre_bits - 1) | 1  # S'assure que c'est bien un nombre de n bits et impair et ou logique avec nombre
        return nombre
    
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
        g = self.__g
        Km = rd.randint(0, p-1)
        self.__Km = Km
        Kp0 = pow(g, Km, p)
        self.__Kp0 = Kp0
        return [Km, Kp0]
        
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


k = DH(x25519,3,500)





