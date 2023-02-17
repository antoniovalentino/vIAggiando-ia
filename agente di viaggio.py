'''
INPUT:
    Azioni svolte dall'agente: stampare una meta di viaggio
    Obiettivo: consigliare una meta di viaggio
    Conoscenze di partenza: varie località con le relative caratteristiche (meteo, cultura, cibo, ambiente)

DURANTE:
    Esperienze precedenti: prende in considerazione gli eventi che sono piaciuti al cliente
    Conoscenze acquisite durante il percorso : preferenze dell'utente in base ai vari filtri, scelta dell'utente
    Stimolo: eventi dati dall'utente ---> fatto
    fare una lista dell'odio e togliere 1 priorità
'''

# Import libraries
import pandas as pd

data = pd.read_csv("travel_data.csv")
preferencesdata = pd.read_csv("preferences_data.csv")
dislikesdata = pd.read_csv("dislikes_data.csv")


def writeFile():
    global data, preferencesdata, dislikesdata
    data.to_csv("travel_data.csv", index=False)
    preferencesdata.to_csv("preferences_data.csv", index=False)
    dislikesdata.to_csv("dislikes_data.csv", index=False)

# funzione di scrittura nel file preference con il controllo se gia è presente prima di scrivere nel file
def addPreferences(pref):
    global preferencesdata
    # controlla se è nella lista dei dislikes prima di scrivere nel file preferiti
    changeDislikeToPreferences(pref)
    preferencesdataList = preferencesdata["preferenze"].tolist()
    if pref not in preferencesdataList:
        preferencesdata.loc[len(preferencesdata)] = [pref]
        return True
    else:
        return False

# controllare se l'elemento preso in input è nella lista dislikes
def changeDislikeToPreferences(pref):
    global dislikesdata
    dislikesdataList = dislikesdata["odio"].tolist()
    if pref in dislikesdataList:
        dislikesdataList.remove(pref)
        dislikesdata = pd.DataFrame(dislikesdataList, columns=['odio'])

# prendere la città che è piaciuta di più e inserisce tutti gli attributi in preferences
def addCityPreferences(ris):
    global data
    like = input("Inserire il nome della destinazione che ti piace di più\n")
    risList=ris["Destinazione"][0:4].tolist()
    if like in risList:
        # troviamo la riga che contiene la città selezionata
        riga = data[data['Destinazione'].str.contains(like)]

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


# funzione per l'eliminazione di una preferenza data in input dall'utente
def delPreferences(pref):
    global preferencesdata
    likes = preferencesdata["preferenze"].tolist()
    if pref in likes:
        likes.remove(pref)
        preferencesdata = pd.DataFrame(likes, columns=['preferenze'])
    else:
        print("la preferenza che vuoi rimuovere non esiste")

def addDislike(dislike):
    changePreferencesToDislikes(dislike)
    global dislikesdata
    dislikesdataList = dislikesdata["odio"].tolist()
    if dislike not in dislikesdataList:
        dislikesdata.loc[len(dislikesdata)] = [dislike]
        return True
    else:
        return False

def changePreferencesToDislikes(dislike):
    global preferencesdata
    preferencesdataList = preferencesdata["preferenze"].tolist()
    if dislike in preferencesdataList:
        preferencesdataList.remove(dislike)
        preferencesdata = pd.DataFrame(preferencesdataList, columns=['preferenze'])

# chiede la città che è piaciuta di meno all'utente
def addCityDislike(ris):
    global dislikesdata
    global data
    dislike = input("Inserire il nome della destinazione che ti piace di meno\n")
    risList = ris["Destinazione"][0:4].tolist()
    if dislike in risList:
        # troviamo la riga che contiene la città selezionata
        riga = data[data['Destinazione'].str.contains(dislike)]
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

# funzione per l'eliminazione di una preferenza
def delDislike(dislike):
    global dislikesdata
    dislikesdataList = dislikesdata["odio"].tolist()
    if dislike in dislikesdataList:
        dislikesdataList.remove(dislike)
        dislikesdata = pd.DataFrame(dislikesdataList, columns=['odio'])
    else:
        print("L'attributo che non preferisci che vuoi rimuovere non esiste")

def isVisited(city):
    global data
    dataList = data["Destinazione"].tolist()
    if city in dataList:
        data.loc[data['Destinazione'] == city, 'Visitato'] = 1
        print(f"Non ti consiglierò più {city} in futuro!\n")
    else:
        print(f"{city} non è tra le città che potrei consigliarti!\n")

# controllo dei preferiti dell'utente e se una determinata città è stata tolta dai preferiti
def vIAggiando():
    global data
    global preferencesdata
    global dislikesdata
    t = {}
    ris = pd.DataFrame(data=t)
    ris.insert(0, "priorità", 0, allow_duplicates=False)

    for row in range(len(data)):
        activities = data.iloc[row]["Attività"]
        weather = data.iloc[row]["Temperatura"]
        ambient = data.iloc[row]["Ambiente"]
        culture = data.iloc[row]["Cultura"]
        food = data.iloc[row]["Cibo tipico"]
        x = 0
        preferences = preferencesdata["preferenze"]
        dislikes = dislikesdata["odio"]

        # controlla se un attributo della città fa parte della lista preferences
        for z in preferences:
            if z in activities or z in weather or z in ambient or z in culture or z in food:
                x += 1

        # controlla se un attributo della città fa parte della lista dislikes
        for z in dislikes:
            if z in activities or z in weather or z in ambient or z in culture or z in food:
                x += 0.5

        vis = data["Visitato"][row:row + 1].tolist()
        # controlla se la destinazione non è apprezzata o già visitata
        if vis[0] != 1:
            ris = pd.concat([ris, data[row:row + 1]], ignore_index=True)
            ris.loc[row, "priorità"] = x

    # stampa QUATTRO soluzioni in base alla priorità che è stata assegnata
    ris = ris.sort_values(by="priorità", ascending=False)
    print(ris[['Destinazione', 'Temperatura', 'Attività', 'Ambiente', 'Cultura', 'Cibo tipico']].head(4),'\n')
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

            # inserisci una preferenza
            preferenza = input("\nInserisci una preferenza da aggiungere o da togliere tra queste categorie:\nattività (es. storica,romantica,moderna)\n"
                               "temperatura (es. piovosa,fresca,calda)\nambiente (es. urbano)\ncultura (es. europea,asiatica,sudamericana)\ncibo tipico (es. pizza,croissant,sushi) \n\n")
            if addPreferences(preferenza):
                print(f"La preferenza {preferenza} è stata aggiunta \n")
            else:
                delPreferences(preferenza)
                print(f"La preferenza {preferenza} è stata eliminata \n")
                # elimina preferenza

        elif scelta == '2':
            global dislikesdata
            print(dislikesdata)
            # inserisci una preferenza
            dislike = input("Inserisci un attributo che non preferisci da togliere o da aggiungere: ")
            if addDislike(dislike):
                print(f"La preferenza {dislike} è stata aggiunta \n")
                # remove dalla lista delle preferenze
            else:
                delDislike(dislike)
                print(f"La prefrenza {dislike} è stata eliminata \n")
                # elimina preferenza

        elif scelta == '3':
            ris = vIAggiando()  # funzione per il consiglio

            is_city_in_ris = False
            while not is_city_in_ris:
                is_city_in_ris = addCityPreferences(ris) # scelta della destinazione preferita tra quelle date a disposizione

            is_city_in_ris = False
            while not is_city_in_ris:
                 is_city_in_ris = addCityDislike(ris)  # scelta della destinazione che è piaciuta di meno all'utente tra quelle date a disposizione

        elif scelta== '4':
            city = input("Inserisci una città già visitata (in modo da evitare che te la consigli) :\n")
            isVisited(city)

        elif scelta == '5':
            x = 1


        else:
            print("Scelta non valida.")

        writeFile()


if __name__ == "__main__":
    main()
