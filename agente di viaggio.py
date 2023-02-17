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

#lettura file csv
def readfile(x):
    data = pd.read_csv("travel_data.csv")
    preferencesdata = pd.read_csv("preferences_data.csv")
    dislikesdata = pd.read_csv("dislikes_data.csv")
    if x == "data":
        return data
    if x == "preferences":
        return preferencesdata
    if x == "dislikes":
        return dislikesdata

# funzione di scrittura nel file preference con il controllo se gia è presente prima di scrivere nel file
def addPreferences(pref):
    # controlla se è nella lista dei dislikes prima di scrivere nel file preferiti
    changeDislikeToPreferences(pref)
    preferencesdata = readfile("preferences")
    preferencesdataList = preferencesdata["preferenze"].tolist()
    if pref not in preferencesdataList:
        preferencesdata.loc[len(preferencesdata)] = [pref]
        preferencesdata.to_csv("preferences_data.csv", index=False)
        return True
    else:
        return False

# controllare se l'elemento preso in input è nella lista dislikes
def changeDislikeToPreferences(pref):
    dislikesdata = readfile("dislikes")
    dislikesdataList = dislikesdata["odio"].tolist()
    if pref in dislikesdataList:
        dislikesdataList.remove(pref)
        t = pd.DataFrame(dislikesdataList, columns=['odio'])
        t.to_csv("dislikes_data.csv", index=False)

# prendere la città che è piaciuta di più e inserisce tutti gli attributi in preferences
def addCityPreferences():
    data = readfile("data")
    like = input("Inserire il nome della destinazione che ti piace di più\n")

    # troviamo la riga che contiene la città selezionata
    riga = data[data['destinazione'].str.contains(like)]

    #richiama la funzione di scrittura nel file preferences
    addPreferences(riga.iloc[0]['attività'])
    addPreferences(riga.iloc[0]['tempo'])
    addPreferences(riga.iloc[0]['ambiente'])
    addPreferences(riga.iloc[0]['cultura'])
    addPreferences(riga.iloc[0]['cibo'])

#funzione per l'eliminazione di una preferenza data in input dall'utente
def delPreferences(pref):
    preferencesdata = readfile("preferences")
    likes = preferencesdata["preferenze"].tolist()
    if pref in likes:
        likes.remove(pref)
        t = pd.DataFrame(likes, columns=['preferenze'])
        t.to_csv("preferences_data.csv", index=False)
    else:
        print("la preferenza che vuoi rimuovere non esiste")

def addDislike(dislike):
    changePreferencesToDislikes(dislike)
    dislikesdata = readfile("dislikes")
    dislikesdataList = dislikesdata["odio"].tolist()
    if dislike not in dislikesdataList:
        dislikesdata.loc[len(dislikesdata)] = [dislike]
        dislikesdata.to_csv("dislikes_data.csv", index=False)
        return True
    else:
        return False

def changePreferencesToDislikes(dislike):
    preferencesdata = readfile("preferences")
    preferencesdataList = preferencesdata["preferenze"].tolist()
    if dislike in preferencesdataList:
        preferencesdataList.remove(dislike)
        t = pd.DataFrame(preferencesdataList, columns=['preferenze'])
        t.to_csv("preferences_data.csv", index=False)

# chiede la città che è piaciuta di meno all'utente
def addCityDislike():
    dislikesdata = readfile("dislikes")
    data = readfile("data")
    dislike = input("Inserire il nome della destinazione che ti piace di meno\n")

    # troviamo la riga che contiene la città selezionata
    riga = data[data['destinazione'].str.contains(dislike)]

    # aggiungiamo una nuova riga alla fine del DataFrame per ogni attvità
    addDislike(riga.iloc[0]['attività'])
    addDislike(riga.iloc[0]['tempo'])
    addDislike(riga.iloc[0]['ambiente'])
    addDislike(riga.iloc[0]['cultura'])
    addDislike(riga.iloc[0]['cibo'])

#funzione per l'eliminazione di una preferenza
def delDislike(dislike):
    dislikesdata = readfile("dislikes")
    dislikesdataList = dislikesdata["odio"].tolist()
    if dislike in dislikesdataList:
        dislikesdataList.remove(dislike)
        t = pd.DataFrame(dislikesdataList, columns=['odio'])
        t.to_csv("dislikes_data.csv", index=False)
    else:
        print("L'attributo che non preferisci che vuoi rimuovere non esiste")

#controllo dei preferiti dell'utente e se una determinata città è stata tolta dai preferiti
def vIAggiando():
    data = readfile("data")
    preferencesdata = readfile("preferences")
    dislikesdata = readfile("dislikes")
    t = {}
    ris = pd.DataFrame(data=t)
    ris.insert(0, "priorità", 0, allow_duplicates=False)

    for row in range(len(data)):
        activities = data.iloc[row]["attività"]
        weather = data.iloc[row]["tempo"]
        ambient = data.iloc[row]["ambiente"]
        culture = data.iloc[row]["cultura"]
        food = data.iloc[row]["cibo"]
        x = 0
        preferences = preferencesdata["preferenze"]
        dislikes = dislikesdata["odio"]

        # controlla se un attributo della città fa parte della lista preferences
        for z in preferences:
            if z in activities:
                x += 1
            if z in weather:
                x += 1
            if z in ambient:
                x += 1
            if z in culture:
                x += 1
            if z in food:
                x += 1

        # controlla se un attributo della città fa parte della lista dislikes
        for z in dislikes:
            if z in activities:
                x -= 0.5
            if z in weather:
                x -= 0.5
            if z in ambient:
                x -= 0.5
            if z in culture:
                x -= 0.5
            if z in food:
                x -= 0.5

        vis = data["preferiti"][row:row + 1].tolist()
        # controlla se la destinazione non è apprezzata o già visitata
        if vis != 1:
            ris = pd.concat([ris, data[row:row + 1]], ignore_index=True)
            ris.loc[row, "priorità"] = x
    # da 4 soluzioni in base alla priorità che è stata assegnata
    ris = ris.sort_values(by="priorità", ascending=False)
    print(ris.head(4))

# IDEA, gli attributi possono avere un numero N nel file, questo numero dice quante volte sono stati preferiti e
# quindi pesano di più quando andiamo a fare i controlli (invece di fare +1 faremo +n)

def main():
    scelta = input(
        "Scegli tra le seguenti opzioni: \n1. Consigliami una destinazione\n2. Modifica le preferenze\n3. Modifica i "
        "dislikes\n")

    if scelta == '1':
        vIAggiando()              #funzione per il consiglio
        addCityPreferences()      #scelta della destinazione preferita tra ####quelle date a disposizione###
        addCityDislike()          #scelta della destinazione che è piaciuta di meno all'utente tra ####quelle date a disposizione###

    elif scelta == '2':
        preferences = readfile("preferences")
        print(preferences)
        #inserisci una preferenza
        preferenza = input("Inserisci una preferenza da togliere o da aggiungere: ")
        if addPreferences(preferenza):
            print(f"La preferenza {preferenza} è stata aggiunta")
        else:
            delPreferences(preferenza)
            print(f"La preferenza {preferenza} è stata eliminata")
            #elimina preferenza

    elif scelta == '3':
        dislikesdata = readfile("dislikes")
        print(dislikesdata)
        # inserisci una preferenza
        dislike = input("Inserisci un attributo che non preferisci da togliere o da aggiungere: ")
        if addDislike(dislike):
            print(f"La preferenza {dislike} è stata aggiunta")
            # remove dalla lista delle preferenze
        else:
            delDislike(dislike)
            print(f"La prefrenza {dislike} è stata eliminata")
            # elimina preferenza
    else:
        print("Scelta non valida.")

if __name__ == "__main__":
    main()