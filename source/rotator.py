# BIBLIOTHEQUES
import socket



def nom():
    """Renvoie le nom de la machine"""
    return socket.gethostname()

def ip():
    """Renvoie l'adresse IPv4 de la machine"""
    return socket.gethostbyname(socket.gethostname())

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











