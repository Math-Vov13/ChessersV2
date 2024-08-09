# Import
import mysql.connector as mySQL
import os
os.environ["DBConnected"] = "False"

# Paramètres de connexion
config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'chessers db'
}

# Connect to DB
try:
    conn = mySQL.connect(**config)
    cursor = conn.cursor()
except Exception as e:
    print("Error while trying to make connection with DataBase :", e)
else:
    print("Connected to DataBase !")
    os.environ["DBConnected"] = "True"


# Fonction pour récupérer une donnée dans la BDD
def getData(Table : str, Attribut : str, Value : str):
    # # Connexion à la base de données
    # conn = mySQL.connect(**config)
    # cursor = conn.cursor()

    # Exécution de la requête
    Requete = f"SELECT * FROM {Table} WHERE {Attribut} = '{Value}'"
    print(Requete)
    cursor.execute(Requete)
    print([i for i in cursor])
    # Récupération de la valeur
    # DataList = cursor.fetchone()
    # print(DataList)
    # Fermeture de la connexion
    #conn.close()

    return [i for i in cursor]

def SaveData(Table : str, Attribut : str, Id : int):
    # # Connexion à la base de données
    # conn = mySQL.connect(**config)
    # cursor = conn.cursor()
    
    Requete = f"UPDATE {Table} SET {Attribut} = {Attribut} + 1 WHERE Id = {Id}"
    print(Requete)
    cursor.execute(Requete)

    # Fermeture de la connexion
    #conn.close()

    return True


def Login(UserName : str, MDP : str):
    Data = getData("comptes", "Pseudonyme", UserName)
    print(Data)
    if not Data:
        return False, "No Account found !", "" #Réussi ?, Message Erreur, Identifiant du Compte
    
    if Data[3] == MDP:
        return True, "", Data[0]
    else:
        return False, "MDP Incorrect !", ""

def SaveGameData(ID : int, Victoire : bool):
    Requete = SaveData("classement", "Parties", ID)
    if Requete == False:
        return False, "Erreur durant la Sauvegarde des Données"
    
    if Victoire == True:
        Requete = SaveData("classement", "Victoires", ID)
        
        if Requete == False:
            return False, "Erreur durant la Sauvegarde des Données"

    return True, "Données Sauvegardées !"

#print(Login("MathV", "MathChess91"))
#print(SaveGameData(1234567890, True))

if __name__ == "__main__":
    if os.environ.get("DBConnected") == "True":
        Requete = f"SELECT * FROM " + "comptes"
        Requete2 = f"SELECT * FROM " + "classement"

        cursor.execute(Requete)
        print("Comptes :", [i for i in cursor])

        cursor.execute(Requete2)
        print("Classements :", [i for i in cursor])

        cursor.close() # Close cursor