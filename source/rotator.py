"""
ROTATOR v1

Plus d'informations sur https://github.com/theofefe22/sae302

"""
# BIBLIOTHEQUES
import socket
import random as rd
from sympy import isprime as isp


# VARIABLES LOCALES
x25519 = ((2**255)-19)
fi = (1+(5**.5))/2


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
            alfa = "1234567890 ABCDEFGH!IJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
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
            nombre = rd.randint(123,8973218)
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
        rds = rd.SystemRandom()
        nombre = 0
        while not isp(nombre): # Tant que le nombre n'est pas premier
            nombre = rd.getrandbits(nombre_bits) # Génère un nombre aléatoire de n bits
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
        Km = rd.randint(0, p-1)
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
    def Km(self) -> int:
        """Renvoie la clé privée"""
        return self.__Km
    
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
        self.__e = e
        # Calcul des coefficients tels que e*u + phi_n*v = pgcd(e,phi_n) = g
        g, u, v = Maths.euclide_etendu(e, phi_n)
        # Calcul du coefficient d
        d = u%phi_n
        self.__d = d
        # Clé privée
        Km = [hex(p), hex(q), hex(d)]
        self.__n = n
        self.__Km = Km
        # Clé publique
        Kp = [hex(n), hex(e)]
        self.__Kp = Kp
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
    
    def hacher(self, message: str) -> hex:
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
    
    def signer(self, message_a_signer: str, Km: list = None) -> list:
        """
        Signe un message
        
        Arguments:
            message_a_signer (str) : Message à signer
            Km (list) : Ma clé privée
        """
        # Caractéristiques du message à signer
        if isinstance(message_a_signer, list):
            message_a_signer = str(message_a_signer)
        # Caractéristiques de ma clé privée
        if Km == None:
            Km = self.__Km
        # Paramètres
        d0 = int(Km[2],16)
        n0 = int(Km[0],16)*int(Km[1],16)
        # Calcul du haché
        hache = int(self.hacher(message_a_signer),16)
        # Cryptage du haché
        signe = pow(hache, d0, n0)
        return [message_a_signer, hex(signe)]
    
    def verifier(self, message_signe: str, Kp1: list = None):
        """
        Vérifie la signature d'un message
        
        Arguments:
            message_signe (str) : Message à signer
            Kp1 (list) : La clé publique de l'autre
        """
        if Kp1 == None:
            Kp1 = self.__Kp1
        message = message_signe[0]
        signe = message_signe[1]
        # Hacher le message reçu
        dessigne_prime = int(self.hacher(message),16)
        print(dessigne_prime)
        # Décripter la signature
        n1 = int(Kp1[0],16)
        e1 = int(Kp1[1],16)
        dessigne = pow(signe, e1, n1)
        print(dessigne)
        # Comparaison
        if dessigne == dessigne_prime:
            print("La signature est correcte !")
            return True
        else:
            print("La signature n'est pas bonne")
            return False


print("Merci d'utiliser ROTATOR")

if __name__ == "__main__":
    print("Tests de fonctionnement")
    kp = rd.randint(0, x25519-1)
    k = DH(x25519,999,kp)
    # Le module os est intégré dans random
    os = rd._os
    os.path.exists('rotator.py')
    h = RSA()
    h.cles(320)
    a = A64()







"""

def conversion(nombre):
    resultat = []
    for i in range:
        
        
    return resultat
        
    
    
   
    quotient, reste = divmod(nombre, 64)
    i
    
    
    
    
    
    while not nombre%64 == 0:
        x = nombre//64
        nombre = nombre%64
        return x
 """   
    








