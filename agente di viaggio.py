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
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier

# dataframe globali che contengono il contenuto dei file
traveldata = pd.read_csv("travel_data.csv")
userdata = pd.read_csv("user_data.csv")

def adesso():
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

    features = ['Attività', 'Temperatura', 'Budget', 'Cultura']

    x = userdata[features]
    y = userdata['Visitato']

    dtree = DecisionTreeClassifier()
    dtree = dtree.fit(x.values, y)

    tree.plot_tree(dtree, feature_names=features)

    z = 0
    for i in range(len(traveldata)):
        if z == 4:
            break
        t = []
        t = dtree.predict([[traveldata["Attività"][i], traveldata["Temperatura"][i], traveldata["Budget"][i], traveldata["Cultura"][i]]])
        if t[0] == 1:
            print(traveldata["Destinazione"][i])
        z = z + t[0]


# funzione per scrivere il contenuto dei dataframe nei file
def writeFile():
    global traveldata, preferencesdata, dislikesdata
    traveldata.to_csv("travel_data.csv", index=False)
    preferencesdata.to_csv("preferences_data.csv", index=False)
    dislikesdata.to_csv("dislikes_data.csv", index=False)


# funzione che aggiunge al dataframe preferencesdata la nuova preferenza presa dal parametro d'ingresso
def addPreferences(pref):
    global preferencesdata
    # controlla se è nella lista dei dislikes prima di scrivere nel dataframe preferencesdata
    changeDislikeToPreferences(pref)
    preferencesdataList = preferencesdata["preferenze"].tolist()
    if pref not in preferencesdataList:
        preferencesdata.loc[len(preferencesdata)] = [pref]
        return True
    else:
        return False


# funzione che controlla se nella lista dei dislikes è presente la preferenza usata come parametro d'ingresso
def changeDislikeToPreferences(pref):
    global dislikesdata
    dislikesdataList = dislikesdata["odio"].tolist()
    if pref in dislikesdataList:
        dislikesdataList.remove(pref)
        dislikesdata = pd.DataFrame(dislikesdataList, columns=['odio'])


# funzione che prende in ingresso una città e aggiunge tutti i suoi attributi a preferencesdata
def addCityPreferences(ris):
    global traveldata
    like = input("Inserire il nome della destinazione che ti piace di più\n")
    risList = ris["Destinazione"][0:4].tolist()
    if like in risList:
        # troviamo la riga che contiene la città selezionata
        riga = traveldata[traveldata['Destinazione'].str.contains(like)]

        # richiama la funzione di scrittura nel file preferences
        addPreferences(riga.iloc[0]['Attività'])
        addPreferences(riga.iloc[0]['Temperatura'])
        addPreferences(riga.iloc[0]['Ambiente'])
        addPreferences(riga.iloc[0]['Cultura'])
        addPreferences(riga.iloc[0]['Cibo tipico'])
        return True
    else:
        print("Scrivi una città tra quelle che ti ho consigliato")
        return False


# funzione per l'eliminazione di una preferenza data in ingresso dall'utente
def delPreferences(pref):
    global preferencesdata
    likes = preferencesdata["preferenze"].tolist()
    if pref in likes:
        likes.remove(pref)
        preferencesdata = pd.DataFrame(likes, columns=['preferenze'])
    else:
        print("la preferenza che vuoi rimuovere non esiste")


# funzione che aggiunge al dataframe dislikesdata il nuovo attributo non preferito preso dal parametro d'ingresso
def addDislike(dislike):
    changePreferencesToDislikes(dislike)
    global dislikesdata
    dislikesdataList = dislikesdata["odio"].tolist()
    if dislike not in dislikesdataList:
        dislikesdata.loc[len(dislikesdata)] = [dislike]
        return True
    else:
        return False


# funzione che controlla se nella lista delle prefrences è presente l'attributo non preferito usato come parametro d'ingresso
def changePreferencesToDislikes(dislike):
    global preferencesdata
    preferencesdataList = preferencesdata["preferenze"].tolist()
    if dislike in preferencesdataList:
        preferencesdataList.remove(dislike)
        preferencesdata = pd.DataFrame(preferencesdataList, columns=['preferenze'])


# funzione che prende in ingresso una città e aggiunge tutti i suoi attributi a dislikesdata
def addCityDislike(ris):
    global dislikesdata
    global traveldata
    dislike = input("Inserire il nome della destinazione che ti piace di meno\n")
    risList = ris["Destinazione"][0:4].tolist()
    if dislike in risList:
        # troviamo la riga che contiene la città selezionata
        riga = traveldata[traveldata['Destinazione'].str.contains(dislike)]
        # aggiungiamo una nuova riga alla fine del DataFrame per ogni attvità
        addDislike(riga.iloc[0]['Attività'])
        addDislike(riga.iloc[0]['Temperatura'])
        addDislike(riga.iloc[0]['Ambiente'])
        addDislike(riga.iloc[0]['Cultura'])
        addDislike(riga.iloc[0]['Cibo tipico'])
        return True
    else:
        print("Scrivi una città tra quelle che ti ho consigliato")
        return False


# funzione per l'eliminazione di un attributo non preferito
def delDislike(dislike):
    global dislikesdata
    dislikesdataList = dislikesdata["odio"].tolist()
    if dislike in dislikesdataList:
        dislikesdataList.remove(dislike)
        dislikesdata = pd.DataFrame(dislikesdataList, columns=['odio'])
    else:
        print("L'attributo che non preferisci che vuoi rimuovere non esiste")

# funzione che marchia come visitata la città usata come parametro d'ingresso
def isVisited(city):
    global traveldata
    dataList = traveldata["Destinazione"].tolist()
    if city in dataList:
        traveldata.loc[traveldata['Destinazione'] == city, 'Visitato'] = 1
        print(f"Non ti consiglierò più {city} in futuro!\n")
    else:
        print(f"{city} non è tra le città che potrei consigliarti!\n")


# funzione che crea i consigli per l'utente
def vIAggiando():
    global traveldata
    global preferencesdata
    global dislikesdata
    t = {}
    ris = pd.DataFrame(data=t)
    ris.insert(0, "priorità", 0, allow_duplicates=False)
    # ciclo for per prendere i singoli attributi delle varie colonne del dataframe
    for row in range(len(traveldata)):

        vis = traveldata["Visitato"][row:row + 1].tolist()
        # controlla se la destinazione è stata già visitata e in quel caso la esclude dalla soluzione
        if vis[0] == 1:
            continue

        activities = traveldata.iloc[row]["Attività"]
        weather = traveldata.iloc[row]["Temperatura"]
        ambient = traveldata.iloc[row]["Ambiente"]
        culture = traveldata.iloc[row]["Cultura"]
        food = traveldata.iloc[row]["Cibo tipico"]
        x = 0
        preferences = preferencesdata["preferenze"]
        dislikes = dislikesdata["odio"]

        # controlla se l'attributo della città fa parte di preferencesdata e in quel caso aumenta la priorità di 1
        for z in preferences:
            if z in activities or z in weather or z in ambient or z in culture or z in food:
                x += 1

        # controlla se l'attributo della città fa parte di dislikesdata e in quel caso abbassa la priorità di 0.5
        for z in dislikes:
            if z in activities or z in weather or z in ambient or z in culture or z in food:
                x += 0.5

        ris = pd.concat([ris, traveldata[row:row + 1]], ignore_index=True)
        ris.loc[row, "priorità"] = x


    # stampa le prime quattro soluzioni in base alla priorità che è stata assegnata
    ris = ris.sort_values(by="priorità", ascending=False)
    print(ris[['Destinazione', 'Temperatura', 'Attività', 'Ambiente', 'Cultura', 'Cibo tipico']].head(4), '\n')
    return ris


# IDEA, gli attributi possono avere un numero N nel file, questo numero dice quante volte sono stati preferiti e
# quindi pesano di più quando andiamo a fare i controlli (invece di fare +1 faremo +n) e serve anche per cancellarlo
# solo se n arriva a 0

def main():
    x = 0
    while x == 0:
        scelta = input(
            "Scegli tra le seguenti opzioni: \n1. Aggiungi/rimuovi le preferenze\n2. Aggiungi/Rimuovi un attributo "
            "che non preferisci\n3. Consigliami una destinazione\n4. Inserisci una città già visitata\n5. Chiudi il programma \n")

        if scelta == '1':
            global preferencesdata

            print("Queste sono le tue preferenze attuali:")
            print(preferencesdata)

            preferenza = input(
                "\nInserisci una preferenza da aggiungere o da togliere tra queste categorie:\nattività (es. storica,romantica,moderna)\n"
                "temperatura (es. piovosa,fresca,calda)\nambiente (es. urbano)\ncultura (es. europea,asiatica,sudamericana)\ncibo tipico (es. pizza,croissant,sushi) \n\n")
            if addPreferences(preferenza):
                print(f"La preferenza {preferenza} è stata aggiunta \n")
            else:
                delPreferences(preferenza)
                print(f"La preferenza {preferenza} è stata eliminata \n")

        elif scelta == '2':
            global dislikesdata
            print(dislikesdata)
            dislike = input("Inserisci un attributo che non preferisci da togliere o da aggiungere: ")
            if addDislike(dislike):
                print(f"La preferenza {dislike} è stata aggiunta \n")
            else:
                delDislike(dislike)
                print(f"La prefrenza {dislike} è stata eliminata \n")

        elif scelta == '3':
            ris = vIAggiando()

            is_city_in_ris = False
            while not is_city_in_ris:
                is_city_in_ris = addCityPreferences(ris)  # scelta della destinazione preferita tra quelle date a disposizione

            is_city_in_ris = False
            while not is_city_in_ris:
                is_city_in_ris = addCityDislike(ris)  # scelta della destinazione che è piaciuta di meno tra quelle date a disposizione

        elif scelta == '4':
            city = input("Inserisci una città già visitata (in modo da evitare che te la consigli) :\n")
            isVisited(city)

        elif scelta == '5':
            x = 1

        else:
            print("Scelta non valida.")

        writeFile() #scrittura dei dati dei dataframe all'interno del file a ogni iterazione del programma


if __name__ == "__main__":
    #print(traveldata['Temperatura'])
    adesso()
