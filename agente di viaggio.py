'''
INPUT:
    Azioni svolte dall'agente: stampare una meta di viaggio
    Obiettivo: consigliare una meta di viaggio
    Conoscenze di partenza: varie località con le relative caratteristiche (meteo, cultura, cibo, ambiente)

DURANTE:
    Esperienze precedenti: prende in considerazione gli eventi che sono piaciuti al cliente
    Conoscenze acquisite durante il percorso : preferenze dell'utente in base ai vari filtri, scelta dell'utente
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


# funzione per scrivere il contenuto dei dataframe nei file
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
    traveldata['Temperatura'] = traveldata['Temperatura'].map(t)
    userdata['Temperatura'] = userdata['Temperatura'].map(t)

    traveldata.to_csv("travel_data.csv", index=False)
    userdata.to_csv("user_data.csv", index=False)


def modDataframe():
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


def vIAggiando():
    global traveldata, userdata
    features = ['Attività', 'Temperatura', 'Budget', 'Cultura']

    X = userdata[features]
    y = userdata['Visitato']

    dtree = DecisionTreeClassifier()
    dtree = dtree.fit(X.values, y)

    tree.plot_tree(dtree, feature_names=features)

    possible_city = []
    ris = []
    z = 0
    for i in range(len(traveldata)):
        if int(dtree.predict([[traveldata["Attività"][i], traveldata["Temperatura"][i], traveldata["Budget"][i],
                               traveldata["Cultura"][i]]])) == 1:
            possible_city.append(traveldata["Destinazione"][i])
    while z < 4:
        choice = random.choice(possible_city)
        if choice not in ris:
            ris.append(choice)
            z += 1
    return ris


# funzione che prende in ingresso una città e aggiunge tutti i suoi attributi a preferencesdata
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
             'Visitato': [1]})
        userdata = pd.concat([userdata, nuova_riga], ignore_index=True)
        return True
    else:
        riga = userdata[userdata['Destinazione'].str.contains(city)]
        if riga.iloc[0]["Visitato"] == 1:
            userdata = userdata.drop(riga.index)
            return False
        else:
            userdata.loc[userdata['Destinazione'] == city, 'Visitato'] = 1
            return True

# funzione che prende in ingresso una città e aggiunge tutti i suoi attributi a dislikesdata
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
             'Visitato': [0]})
        userdata = pd.concat([userdata, nuova_riga], ignore_index=True)
        return True
    else:
        riga = userdata[userdata['Destinazione'].str.contains(city)]
        if riga.iloc[0]["Visitato"] == 0:
            userdata = userdata.drop(riga.index)
            return False
        else:
            userdata.loc[userdata['Destinazione'] == city, 'Visitato'] = 0
            return True

# IDEA, gli attributi possono avere un numero N nel file, questo numero dice quante volte sono stati preferiti e
# quindi pesano di più quando andiamo a fare i controlli (invece di fare +1 faremo +n) e serve anche per cancellarlo
# solo se n arriva a 0

def main():
    global userdata, traveldata
    x = 0
    while x == 0:
        modDataframe()
        scelta = input(
            "Scegli tra le seguenti opzioni: \n1. Aggiungi/Rimuovi una città che ti piace\n2. Aggiungi/Rimuovi una città che non ti piace\n3. Consigliami una destinazione\n4. Chiudi il programma \n")

        if scelta == '1':

            print('Queste sono le città che ti piacciono attualmente:')
            print(userdata.loc[userdata['Visitato'] == 1, 'Destinazione'])  # stampa solo le righe con 1
                                # adesso bisogna fare che il programma controlla solo nella lista degli 1 e
                                #  non in tutto userdata quando chiamo addcitypreferences
            city = input(
                f"\nInserisci una città che preferisci tra queste:\n{traveldata['Destinazione']}\n"
                f"Per rimuovere una città scrivi un nome già presente nella lista\n")

            if addCityPreferences(city):
                print(f"{city} è stata aggiunta\n")
            else:
                print(f"{city} è stata rimossa\n")

        elif scelta == '2':

            print('Queste sono le città che non ti piacciono attualmente:')
            print(userdata.loc[userdata['Visitato'] == 0, 'Destinazione'])  # stampa solo le righe con 0
                                 # adesso bisogna fare che il programma controlla solo nella lista degli 1 e
                                 #  non in tutto userdata quando chiamo addcitydislike
            city = input(
                f"\nInserisci una città che non ti piace tra queste:\n{traveldata['Destinazione']}\n"
                f"Per rimuovere una città scrivi un nome già presente nella lista\n")

            if addCityDislike(city):
                print(f"{city} è stata aggiunta\n")
            else:
                print(f"{city} è stata rimossa \n")

        elif scelta == '3':
            ris = vIAggiando()
            print("Ecco i miei consigli per te:")
            for item in ris:
                print("- " + item)
            f = False
            while not f:
                city = input("Inserisci la città che ti piace di più\n")
                if city in ris:
                    addCityPreferences(city)  # scelta della destinazione preferita tra quelle date a disposizione
                    f = True
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
