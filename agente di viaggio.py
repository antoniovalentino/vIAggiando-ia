'''
INPUT:
    Azioni svolte dall'agente: stampare una meta di viaggio
    Obiettivo: consigliare una meta di viaggio
    Conoscenze di partenza: varie località con le relative caratteristiche (meteo, cultura, cibo, ambiente)

DURANTE:
    Esperienze precedenti: prende in considerazione gli eventi che sono piaciuti al cliente
    Conoscenze acquisite durante il percorso: preferenze dell'utente in base ai vari filtri, scelta dell'utente
    Stimolo: eventi dati dall'utente
    fare una lista dell'odio e togliere 1 priorità
'''

# Import libraries
import pandas as pd
import random
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier

# dataframe globali che contengono il contenuto dei file
traveldata = pd.read_csv("travel_data.csv")
userdata = pd.read_csv("user_data.csv")

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
    traveldata['Temperatura'] = traveldata['Temperatura'].map(t) #Pandas has a map() method that takes a dictionary with information on how to convert the values.
    userdata['Temperatura'] = userdata['Temperatura'].map(t) #Pandas has a map() method that takes a dictionary with information on how to convert the values.
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

# funzione che genera quattro consigli di città che l'utente visiterebbe, utilizzando i decision tree
def vIAggiando():
    global traveldata, userdata
    features = ['Attività', 'Temperatura', 'Budget', 'Cultura']

    X = userdata[features]   # The feature columns are the columns that we try to predict from, and the target column is the column with the values we try to predict
    y = userdata['Visiterei'] ####################################################################

    dtree = DecisionTreeClassifier() # creazione decision tree
    dtree = dtree.fit(X.values, y) # Now we can create the actual decision tree, fit it with our details. Start by importing the modules we need:

    tree.plot_tree(dtree, feature_names=features)

    possible_city = []  # lista di tutte le città che l'utente visiterebbe secondo il decision tree
    ris = []    # lista che contiene i quattro consigli dell'agente
    z = 0
    for i in range(len(traveldata)):
        # predict sul decision tree con i dati di ogni città presente nel file travel_data
        if int(dtree.predict([[traveldata["Attività"][i], traveldata["Temperatura"][i], traveldata["Budget"][i],
                               traveldata["Cultura"][i]]])) == 1:
            possible_city.append(traveldata["Destinazione"][i])
    # ciclo while nel quale vengono scelte quattro città all'interno della lista possible_city
    while z < 4:
        choice = random.choice(possible_city)
        if choice not in ris:   # verifica che la scelta non faccia già parte del risultato
            ris.append(choice)
            z += 1
    return ris  # ritorna le quattro scelte


# funzione che prende in ingresso una città e nel caso non è presente nel dataframe userdata la aggiunge,
# nel caso fosse presente con Visiterei = 1 viene rimossa,
# nel caso fosse presente con Visiterei = 0 viene modificato il valore portandolo a 1
def addCityPreferences(city):
    global traveldata, userdata
    userdataList = userdata['Destinazione'].tolist()

    if city not in userdataList:
        # troviamo la riga che contiene la città selezionata
        riga = traveldata[traveldata['Destinazione'].str.contains(city)]

        nuova_riga = pd.DataFrame(
            {'Destinazione': [riga.iloc[0]['Destinazione']], 'Attività': [riga.iloc[0]['Attività']],
             'Temperatura': [riga.iloc[0]['Temperatura']],
             'Budget': [riga.iloc[0]['Budget']], 'Cultura': [riga.iloc[0]['Cultura']],
             'Visiterei': [1]})
        userdata = pd.concat([userdata, nuova_riga], ignore_index=True)
        return True
    else:
        riga = userdata[userdata['Destinazione'].str.contains(city)]
        if riga.iloc[0]["Visiterei"] == 1:
            userdata = userdata.drop(riga.index)
            return False
        else:
            userdata.loc[userdata['Destinazione'] == city, 'Visiterei'] = 1
            return True


# funzione che prende in ingresso una città e nel caso non è presente nel dataframe userdata la aggiunge,
# nel caso fosse presente con Visiterei = 0 viene rimossa,
# nel caso fosse presente con Visiterei = 1 viene modificato il valore portandolo a 0
def addCityDislike(city):
    global traveldata, userdata
    userdataList = userdata['Destinazione'].tolist()
    if city not in userdataList:
        # troviamo la riga che contiene la città selezionata
        riga = traveldata[traveldata['Destinazione'].str.contains(city)]

        nuova_riga = pd.DataFrame(
            {'Destinazione': [riga.iloc[0]['Destinazione']], 'Attività': [riga.iloc[0]['Attività']],
             'Temperatura': [riga.iloc[0]['Temperatura']],
             'Budget': [riga.iloc[0]['Budget']], 'Cultura': [riga.iloc[0]['Cultura']],
             'Visiterei': [0]})
        userdata = pd.concat([userdata, nuova_riga], ignore_index=True)
        return True
    else:
        riga = userdata[userdata['Destinazione'].str.contains(city)]
        if riga.iloc[0]["Visiterei"] == 0:
            userdata = userdata.drop(riga.index)
            return False
        else:
            userdata.loc[userdata['Destinazione'] == city, 'Visiterei'] = 0
            return True


def main():
    global userdata, traveldata
    x = 0
    while x == 0:
        numerizeDataframe()
        scelta = input(
            "Scegli tra le seguenti opzioni: \n1. Aggiungi/Rimuovi una città che visiteresti\n"
            "2. Aggiungi/Rimuovi una città che non visiteresti\n3. Consigliami una destinazione\n"
            "4. Chiudi il programma \n")

        if scelta == '1':
            # stampa tutte le città salvate nel file
            print(f"\nQuesta è la lista delle città disponibili:\n{traveldata['Destinazione']}\n")

            print('Queste sono le città che visiteresti:')
            # stampa solo le righe con 1
            print(userdata.loc[userdata['Visiterei'] == 1, 'Destinazione'], '\n')

            city = input(
                "Scrivi una città che visiteresti, "
                "per rimuovere una città scrivi un nome già presente nella lista delle città che visiteresti\n")

            if addCityPreferences(city):
                print(f"{city} è stata aggiunta\n")
            else:
                print(f"{city} è stata rimossa\n")

        elif scelta == '2':
            # stampa tutte le città salvate nel file
            print(f"\nQuesta è la lista delle città disponibili:\n{traveldata['Destinazione']}\n")

            print('Queste sono le città che non visiteresti:')
            # stampa solo le righe con 0
            print(userdata.loc[userdata['Visiterei'] == 0, 'Destinazione'], '\n')

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
                    addCityPreferences(city)
                    f = True
                    print(f"{city} è stata aggiunta tra quelle che visiteresti\n")
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
