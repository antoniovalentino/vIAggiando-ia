import random
from collections import deque

# Import libraries
import pandas as pd
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier

# dataframe globali che contengono il contenuto dei file
traveldata = pd.read_csv("travel_data.csv")
userdata = pd.read_csv("user_data.csv")

# matrice di tutte le città
cityM = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
]

# dizionario di associazione (città,pixel della matrice)
cityD = {
    'Roma': (0, 0),
    'Londra': (0, 1),
    'Parigi': (0, 2),
    'Tokyo': (0, 3),
    'New York': (0, 4),
    'Barcellona': (0, 5),
    'Città del Messico': (0, 6),
    'Berlino': (1, 0),
    'Sidney': (1, 1),
    'Rio de Janeiro': (1, 2),
    'Bangkok': (1, 3),
    'Amsterdam': (1, 4),
    'San Francisco': (1, 5),
    'Madrid': (1, 6),
    'Dubai': (2, 0),
    'Mumbai': (2, 1),
    'Vienna': (2, 2),
    'Seoul': (2, 3),
    'Firenze': (2, 4),
    'Los Angeles': (2, 5),
    'Hong Kong': (2, 6),
    'Istanbul': (3, 0),
    'Toronto': (3, 1),
    'San Paolo': (3, 2),
    'Shanghai': (3, 3),
    'Venezia': (3, 4),
    'Napoli': (3, 5),
    'Matera': (3, 6),
    'Bologna': (4, 0),
    'Palermo': (4, 1),
    'Verona': (4, 2),
    'Genova': (4, 3),
    'Lecce': (4, 4),
    'Trieste': (4, 5),
    'Helsinki': (4, 6),
    'Rio Grande': (5, 0),
    'Marrakech': (5, 1),
    'Honolulu': (5, 2),
    'Lisbona': (5, 3),
    'Dublino': (5, 4),
    'Buenos Aires': (5, 5),
    'Atene': (5, 6),
    'Reykjavik': (6, 0),
    'Chiang Mai': (6, 1),
    'Vancouver': (6, 2),
    'Taipei': (6, 3),
    'Salonicco': (6, 4),
    'Austin': (6, 5),
    'Copenhagen': (6, 6)
}


# funzione per scrivere il contenuto dei dataframe nei file,
# prima di scrivere converte i dati dei dataframe da numeri a parole
def writeFile():
    global traveldata, userdata
    a = {
        0: "storica",
        1: "romantica",
        2: "moderna",
        3: "multiculturale",
        4: "artistica",
        5: "alternativa",
        6: "costiera",
        7: "tropicale",
        8: "caotica",
        9: "trendy",
        10: "lussuosa",
        11: "divertente",
        12: "accogliente",
        13: "vivace",
        14: "barocca",
        15: "minimalista",
        16: "esotica",
        17: "rilassante"
    }
    traveldata['Attività'] = traveldata['Attività'].map(a)
    userdata['Attività'] = userdata['Attività'].map(a)

    b = {
        0: "basso",
        1: "medio",
        2: "alto"
    }
    traveldata['Budget'] = traveldata['Budget'].map(b)
    userdata['Budget'] = userdata['Budget'].map(b)

    c = {
        0: 'europea',
        1: 'asiatica',
        2: 'americana',
        3: 'nordamericana',
        4: 'australiana',
        5: 'sudamericana',
        6: 'medio orientale',
        7: 'africana'
    }
    traveldata['Cultura'] = traveldata['Cultura'].map(c)
    userdata['Cultura'] = userdata['Cultura'].map(c)

    t = {
        0: 'fredda',
        1: 'mite',
        2: 'calda'

    }
    traveldata['Temperatura'] = traveldata['Temperatura'].map(
        t)  # Pandas has a map() method that takes a dictionary with information on how to convert the values.
    userdata['Temperatura'] = userdata['Temperatura'].map(
        t)  # Pandas has a map() method that takes a dictionary with information on how to convert the values.
    ###############################################################################
    traveldata.to_csv("travel_data.csv", index=False)
    userdata.to_csv("user_data.csv", index=False)


# funzione per convertire i dati dei dataframe da parole a numeri
def numerizeDataframe():
    a = {
        "storica": 0,
        "romantica": 1,
        "moderna": 2,
        "multiculturale": 3,
        "artistica": 4,
        "alternativa": 5,
        "costiera": 6,
        "tropicale": 7,
        "caotica": 8,
        "trendy": 9,
        "lussuosa": 10,
        "divertente": 11,
        "accogliente": 12,
        "vivace": 13,
        "barocca": 14,
        "minimalista": 15,
        "esotica": 16,
        "rilassante": 17
    }
    traveldata['Attività'] = traveldata['Attività'].map(a)
    userdata['Attività'] = userdata['Attività'].map(a)

    b = {
        "basso": 0,
        "medio": 1,
        "alto": 2
    }
    traveldata['Budget'] = traveldata['Budget'].map(b)
    userdata['Budget'] = userdata['Budget'].map(b)

    c = {
        'europea': 0,
        'asiatica': 1,
        'americana': 2,
        'nordamericana': 3,
        'australiana': 4,
        'sudamericana': 5,
        'medio orientale': 6,
        'africana': 7
    }
    traveldata['Cultura'] = traveldata['Cultura'].map(c)
    userdata['Cultura'] = userdata['Cultura'].map(c)

    t = {
        'fredda': 0,
        'mite': 1,
        'calda': 2

    }
    traveldata['Temperatura'] = traveldata['Temperatura'].map(t)
    userdata['Temperatura'] = userdata['Temperatura'].map(t)


# funzione che genera la matrice delle città, mettendo 1 a quelle che non visiteresti
def setCityM():
    global cityM, cityD, userdata
    userdataList = userdata["Destinazione"].tolist()

    for i in cityD:
        if i in userdataList:
            riga = userdata[userdata['Destinazione'].str.contains(i)]
            val = riga["Visiterei"].tolist()
            if val[0] == 0:
                cityM[cityD[i][0]][cityD[i][1]] = 1


# funzione che genera quattro consigli di città che l'utente visiterebbe, utilizzando i decision tree
def vIAggiando():
    global traveldata, userdata
    features = ['Attività', 'Temperatura', 'Budget', 'Cultura']

    X = userdata[
        features]  # Le colonne "features" sono le colonne dalle quali proviamo a fare la predizione e la colonna "visiterei" è la colonna con il valore che proviamo a predirre
    y = userdata['Visiterei']

    dtree = DecisionTreeClassifier()  # creazione decision tree
    dtree = dtree.fit(X.values,
                      y)   # Ora possiamo creare l'attuale decision tree, adattato ai nostri dettagli.

    possible_city = []  # lista di tutte le città che l'utente visiterebbe secondo il decision tree
    ris = []  # lista che contiene i quattro consigli dell'agente
    z = 0
    for i in range(len(traveldata)):
        # predict sul decision tree con i dati di ogni città presente nel file travel_data
        if dtree.predict([[traveldata["Attività"][i], traveldata["Temperatura"][i], traveldata["Budget"][i],
                               traveldata["Cultura"][i]]]) == 1:
            possible_city.append(traveldata["Destinazione"][i])
    # ciclo while nel quale vengono scelte quattro città all'interno della lista possible_city
    while z < 4:
        choice = random.choice(possible_city)
        if choice not in ris:  # verifica che la scelta non faccia già parte del risultato
            ris.append(choice)
            z += 1
    return ris  # ritorna le quattro scelte


# funzione che prende in ingresso una città e nel caso non è presente nel dataframe userdata la aggiunge,
# nel caso fosse presente con Visiterei = 1 viene rimossa,
# nel caso fosse presente con Visiterei = 0 viene modificato il valore portandolo a 1
def addCityPreferences(city, verify):
    global traveldata, userdata, cityM, cityD
    userdataList = userdata['Destinazione'].tolist()

    if city not in userdataList:

        # troviamo la riga che contiene la città selezionata e la copiamo con 'Visiterei' impostato a 1
        nuova_riga = traveldata.loc[traveldata['Destinazione'].str.contains(city)].iloc[[0], :].copy()
        nuova_riga['Visiterei'] = 1

        userdata = pd.concat([userdata, nuova_riga], ignore_index=True)
        # modifica il valore nella matrice della città scelta come da visitare
        cityM[cityD[city][0]][cityD[city][1]] = 0

        return True
    # l' else viene eseguito solo nel caso in cui il metodo è stato richiamato dal numero 1 del menu
    elif verify:

        riga = userdata[userdata['Destinazione'].str.contains(city)]
        if riga.iloc[0]["Visiterei"] == 1:
            userdata = userdata.drop(riga.index)
        else:
            userdata.loc[userdata['Destinazione'] == city, 'Visiterei'] = 1

        # modifica il valore nella matrice della città scelta come da visitare
        cityM[cityD[city][0]][cityD[city][1]] = 0
        # return True se Visiterei = 0 e False se Visiterei = 1
        return riga.iloc[0]["Visiterei"] != 1

    return True


# funzione che prende in ingresso una città e nel caso non è presente nel dataframe userdata la aggiunge,
# nel caso fosse presente con Visiterei = 0 viene rimossa,
# nel caso fosse presente con Visiterei = 1 viene modificato il valore portandolo a 0
def addCityDislike(city):
    global traveldata, userdata, cityM, cityD
    userdataList = userdata['Destinazione'].tolist()
    if city not in userdataList:

        # troviamo la riga che contiene la città selezionata e la copiamo con 'Visiterei' impostato a 0
        nuova_riga = traveldata.loc[traveldata['Destinazione'].str.contains(city)].iloc[[0], :].copy()
        nuova_riga['Visiterei'] = 0

        userdata = pd.concat([userdata, nuova_riga], ignore_index=True)

        # modifica il valore nella matrice della città scelta come da non visitare
        cityM[cityD[city][0]][cityD[city][1]] = 1

        return True
    else:
        riga = userdata[userdata['Destinazione'].str.contains(city)]
        if riga.iloc[0]["Visiterei"] == 0:
            userdata = userdata.drop(riga.index)
            # modifica il valore nella matrice della città scelta come da non visitare
            cityM[cityD[city][0]][cityD[city][1]] = 0

        else:
            userdata.loc[userdata['Destinazione'] == city, 'Visiterei'] = 0
            # modifica il valore nella matrice della città scelta come da non visitare
            cityM[cityD[city][0]][cityD[city][1]] = 1
        # return True se Visiterei = 1 e False se Visiterei = 0
        return riga.iloc[0]["Visiterei"] != 0


# Verifica se è possibile andare al pixel (x, y) dall'attuale
# pixel. La funzione restituisce false se il pixel non è valido
def isSafe(mat, x, y):
    return 0 <= x < len(mat) and 0 <= y < len(mat[0]) and mat[x][y] == 0


# Verifica se il pixel (x, y) è il goal da raggiungere
def isGoal(x, y, xG, yG):
    if (x == xG and y == yG):
        return True
    else:
        return False


# Trova il path più breve tra le due città usando BFS
def cityPath(cityM, x, y, xG, yG):
    # Lista di tutte gli otto possibili movimenti
    row = [-1, -1, -1, 0, 0, 1, 1, 1]
    col = [-1, 0, 1, -1, 1, -1, 0, 1]

    # caso base
    if not cityM or not len(cityM):
        return

    # crea una coda e mette in coda il pixel di partenza
    q = deque()
    q.append(((x, y), [(x, y)]))

    # break quando la coda è vuota
    while q:
        # toglie dalla coda il nodo frontale e lo processa
        (x, y), path = q.popleft()

        # processa gli otto pixel adiacenti all'attuale pixel e
        # aggiunge ogni pixel valido alla coda
        for k in range(len(row)):
            # verifica se il pixel nella posizione (x + row[k], y + col[k]) è il goal
            # e nel caso termina la ricerca del path
            if isGoal(x + row[k], y + col[k], xG, yG):
                return path + [(x + row[k], y + col[k])]
            # verifica se il pixel adiacente nella posizione (x + row[k], y + col[k]) è valido
            if isSafe(cityM, x + row[k], y + col[k]):
                # aggiunge il pixel adiacente
                q.append(((x + row[k], y + col[k]), path + [(x + row[k], y + col[k])]))

    print("Non esiste nessun path")


def coupleCity(cityStart, cityDest):
    global cityM, cityD
    # ottiene la coppia (x, y) della città di partenza
    x = cityD[cityStart][0]
    y = cityD[cityStart][1]
    # ottiene la coppia (x, y) della città di desinazione
    xG = cityD[cityDest][0]
    yG = cityD[cityDest][1]

    cityPathQueue = cityPath(cityM, x, y, xG, yG)
    cityPathList = []
    for i in cityPathQueue:
        for k, v in cityD.items():
            if v == i:
                cityPathList.append(k)

    stringa = " ---> ".join(cityPathList)
    print(stringa)


def main():
    global userdata, traveldata
    x = 0
    while x == 0:
        setCityM()
        numerizeDataframe()
        scelta = input(
            "Scegli tra le seguenti opzioni: \n1. Aggiungi/Rimuovi una città che visiteresti\n"
            "2. Aggiungi/Rimuovi una città che non visiteresti\n3. Consigliami una destinazione\n"
            "4. Chiudi il programma \n")

        if scelta == '1':
            # stampa tutte le città salvate nel file
            print(f"\nQuesta è la lista delle città disponibili:\n{traveldata['Destinazione'].to_string(index=False)}\n")

            print('Queste sono le città che visiteresti:')
            # stampa solo le righe con 1
            df = userdata.loc[userdata['Visiterei'] == 1, 'Destinazione']
            print(df.to_string(index=False), '\n')

            city = input(
                "Scrivi una città che visiteresti, "
                "per rimuovere una città scrivi un nome già presente nella lista delle città che visiteresti\n")

            if addCityPreferences(city, True):
                print(f"{city} è stata aggiunta\n")
            else:
                print(f"{city} è stata rimossa\n")

        elif scelta == '2':
            # stampa tutte le città salvate nel file
            print(f"\nQuesta è la lista delle città disponibili:\n{traveldata['Destinazione'].to_string(index=False)}\n")

            print('Queste sono le città che non visiteresti:')
            # stampa solo le righe con 0
            df = userdata.loc[userdata['Visiterei'] == 0, 'Destinazione']
            print(df.to_string(index=False), '\n')

            city = input(
                "Scrivi una città che non visiteresti, "
                "per rimuovere una città scrivi un nome già presente nella lista delle città che non visiteresti\n")

            if addCityDislike(city):
                print(f"{city} è stata aggiunta\n")
            else:
                print(f"{city} è stata rimossa \n")

        elif scelta == '3':
            ris = vIAggiando()
            # stampa i consigli ottenuti dalla funzione vIAggiando
            print("Ecco i miei consigli per te:")
            for item in ris:
                print("- " + item)
            f = False
            # scelta della destinazione preferita tra quelle date a disposizione,
            # nel caso ne sceglie una non presente nei consigli deve reinserire la scelta
            while not f:
                city = input("Inserisci la città che ti piace di più\n")
                if city in ris:
                    addCityPreferences(city, False)
                    f = True
                    print(f"{city} è stata aggiunta tra quelle che visiteresti\n")

                    print(
                        f"\nVorrei consigliarti un percorso di città per arrivare alla tua selta, ovviamente evitando quelle che non visiteresti,\n"
                        f"Da quale città vorresti partire? Ecco la lista delle città disponibili:\n{traveldata['Destinazione']}")
                    response = False
                    while not response:
                        cityStart = input("")
                        if cityStart in traveldata['Destinazione'].tolist():
                            response = True
                            coupleCity(cityStart, city)
                        else :
                            print("Error: Scrivi una città tra quelle della lista!\n")

                else:
                    print("Error: Scrivi una città tra quelle che ti ho consigliato!\n")

        elif scelta == '4':
            print("Ciao utente, alla prossima esecuzione!")
            x = 1

        else:
            print("Scelta non valida.")

        writeFile()  # scrittura dei dati dei dataframe all'interno del file a ogni iterazione del programma


if __name__ == "__main__":
    main()
