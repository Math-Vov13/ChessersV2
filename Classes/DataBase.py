# Import
import aiomysql # mySQL with asyncio
from aiomysql.cursors import Error as mySQL_Errors # mySQL errors
import asyncio # asynchronous programing
import os # Set env variable
os.environ["DBConnected"] = "False"


# TRANSFORM TO API !


# Paramètres de connexion
config = {
    "user": 'root',
    "password": os.environ.get("MYPASS", 'root'),
    "host": '127.0.0.1', # localhost
    "db": 'chessers db',

    # useless ?
    # "use_pure": True,
    # "port": 3306,
}

# conn = None
# cursor = None

# Connect to DB
async def Connect_toDB():    
    try:
        conn = await aiomysql.connect(**config)
        cursor = await conn.cursor()
        await cursor.close()
    except Exception as e:
        print("Error while trying to make connection with DataBase :", e)
    else:
        print("Connected to DataBase !")
        os.environ["DBConnected"] = "True"



# Fonction pour récupérer une donnée dans la BDD
async def getData(Table : str, Attribut : str, Value : str):
    if os.environ.get("DBConnected") == "False":
        return False
    
    try:
        async with await aiomysql.connect(**config) as cnx:
            async with await cnx.cursor() as cur:

                # Exécution de la requête
                Request = f"SELECT * FROM {Table} WHERE {Attribut} = '{Value}'"
                print(Request)

                await cur.execute(Request)
                Results = cur.fetchall()

                return Results
    
    except mySQL_Errors as mySQL_err:
        print("Error while trying to make connection with DataBase :", mySQL_err)
        return False
    except Exception as e:
        print("Exception error :", e)
        return False

async def SaveData(Table : str, Attribut : str, Id : int):
    if os.environ.get("DBConnected") == "False":
        return False
    
    try:
        async with await aiomysql.connect(**config) as cnx:
            async with await cnx.cursor() as cur:
                Request = f"UPDATE {Table} SET {Attribut} = {Attribut} + 1 WHERE Id = {Id}"
                print(Request)

                await cur.execute(Request)
                
                return True
    
    except mySQL_Errors as mySQL_err:
        print("Error while trying to make connection with DataBase :", mySQL_err)
        return False
    except Exception as e:
        print("Exception error :", e)
        return False


async def Login(UserName : str, MDP : str):
    if os.environ.get("DBConnected") == "False":
        return False
    
    Data = await getData("comptes", "Pseudonyme", UserName)
    print(Data)
    if not Data:
        return False, "No Account found !", "" #Réussi ?, Message Erreur, Identifiant du Compte
    
    if Data[3] == MDP:
        return True, "", Data[0]
    else:
        return False, "MDP Incorrect !", ""

async def SaveGameData(ID : int, Victoire : bool):
    if os.environ.get("DBConnected") == "False":
        return False

    Requete = await SaveData("classement", "Parties", ID)
    if Requete == False:
        return False, "Erreur durant la Sauvegarde des Données"
    
    if Victoire == True:
        Requete = await SaveData("classement", "Victoires", ID)
        
        if Requete == False:
            return False, "Erreur durant la Sauvegarde des Données"

    return True, "Données Sauvegardées !"


if __name__ == "__main__":
    async def makeTests():
        # Create requests
        Request = f"SELECT * FROM comptes"
        Request2 = f"SELECT * FROM classement"

        try:
            async with await aiomysql.connect(**config) as cnx:
                async with await cnx.cursor() as cur:
                    # Execute a non-blocking query
                    await cur.execute(Request)

                    # Retrieve the results of the query asynchronously
                    results = await cur.fetchall()
                    print("Comptes :", results)

                    # Execute a non-blocking query
                    await cur.execute(Request2)

                    # Retrieve the results of the query asynchronously
                    results = await cur.fetchall()
                    print("Classements :", results)

        except mySQL_Errors as mySQL_err:
            print("Error while trying to make connection with DataBase :", mySQL_err)
        except Exception as e:
            print("Exception error :", e)

        else:
            print("Test passed !")
    
    asyncio.create_task(makeTests())
else:
    asyncio.run(Connect_toDB())