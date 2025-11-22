# Bibliothèques à importer
import mysql.connector

# Connexion à la base de données
BDD = mysql.connector.connect(host="localhost",user="master1",password="JEsuisLEmaitre1", database="sae302_tests_01")
cursor = BDD.cursor()
#cursor.execute("CREATE TABLE Produits (reference CHAR(5) NOT NULL PRIMARY KEY, nom TINYTEXT NOT NULL, prix FLOAT NOT NULL)ENGINE=InnoDB DEFAULT CHARSET=utf8;")
BDD.close()


"""
Clé de chiffrement envoyée aux routeurs
"""
fi = (1+5**.5)/2
fi = str(fi)
fi = fi[2:]
fim = [[fi[0],fi[1],fi[2],fi[3],fi[4]], [fi[5],fi[6],fi[7],fi[8],fi[9]], [fi[10],fi[11],fi[12],fi[13],fi[14]]]

print(f"La Clé est : {fi}")
for ligne in fim:
    print(ligne)



















#i,j = 3,3 # Nombre de routeurs


i = j = 3

vz1 = [[2 for _ in range(j)] for _ in range(i)]

for ligne in vz1:
    print(ligne)


def vz(x):
    #for i in range(x):
    #    print(f"Un routeur a été ajouté")
    
    print(f"Les paramètres de {x} sont : ")




ip1 = [128,19,80,2]
masque = [255,255,0,0]
reseau = []

for i in range(0,4):
    reseau.append(ip1[i] & masque[i])
print(f"Le réseau est {reseau}")

reseau1 = [123,12,0,0]


if reseau == reseau1:
    print("OK")
else:
    print("Non, vous n'êtes pas sur le même réseau !")








