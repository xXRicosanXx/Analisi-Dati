import folium
import json

def stazioni(): #qua crea il file CHE ci dice cosa le varie stazione analizzino + mappa stazioni folium
    with open("Stazioni.json", "r") as file:
        stazioni_data = json.load(file)

    proprietà = []

    for feature in stazioni_data["features"]:
        proprietà.append([{"Stazione ID": feature["properties"]["id_amat"]}, {"Inquinante": feature["properties"]["inquinanti"]} , {"Longitudine": feature["properties"]["LONG_X_4326"]}, {"Latitudine": feature["properties"]["LAT_Y_4326"]}])

    print(proprietà)

    with open("proprietà_stazioni.json", "w") as outfile:
        json.dump(proprietà, outfile)

    FINALE = []

    for proprietà in proprietà:
        s = proprietà[1]["Inquinante"]
        lista = [x.strip() for x in s.split(",")]
        print(lista)
        proprietà[1]["Inquinante"] = lista
        FINALE.append(proprietà)

    with open("proprietà_stazioni.json", "w") as outfile:
        json.dump(FINALE, outfile)

    mappa = folium.Map(location=[45.4773, 9.1815], zoom_start=11.75)
    for feature in stazioni_data["features"]:
        latitudine = feature["properties"]["LAT_Y_4326"]
        longitudine = feature["properties"]["LONG_X_4326"]
        nome_stazione = feature["properties"]["id_amat"]
        inquinante = feature["properties"]["inquinanti"]
        
        popup_info = f"Stazione ID: {nome_stazione}<br>Inquinante: {inquinante}"
        
        folium.Marker(
            location=[latitudine, longitudine],
            popup=popup_info
        ).add_to(mappa)

    mappa.save("mappa_stazioni.html")




def che_inquinanti_ci_sono(): #cosi vediamo che inqunantile stazioni vedono
    with open("proprietà_stazioni.json", "r") as file:
        Stazioni = json.load(file)

    inquinanti_analizzati = []

    for stazione in Stazioni:
        inquinanti = stazione[1]["Inquinante"]
        for inquinante in inquinanti:
            if inquinante not in inquinanti_analizzati:
                inquinanti_analizzati.append(inquinante)

    print("\n")
    print(inquinanti_analizzati)





def carica_dati_Qaria(): #questa funzione ci crea un file che poi ci faciliterà l'analizzazione.
    Qaria_dati = {}
    for stazione_id in range(1, 10): 
        print(f"\nCaricamento stazione {stazione_id}")
        Qaria_dati[str(stazione_id)] = {}
        
        for anno in range(2015, 2026):
                with open(f"Qaria-{anno}.json", "r") as file:
                    Qaria = json.load(file)
                
                for elementi in Qaria:
                    if elementi["stazione_id"] == str(stazione_id):
                        data = elementi["data"]
                        inquinante = elementi["inquinante"]
                        valore = elementi["valore"]
                        
                        if data not in Qaria_dati[str(stazione_id)]:
                            Qaria_dati[str(stazione_id)][data] = {}
                        
                        Qaria_dati[str(stazione_id)][data][inquinante] = valore
                
                print(f"  Caricato Qaria-{anno}.json")



    Qaria_dati_ordinato = {}
    for stazione_id in sorted(Qaria_dati.keys(), key=lambda x: int(x)):
        Qaria_dati_ordinato[stazione_id] = Qaria_dati[stazione_id]

    with open("Qaria_dati.json", "w") as outfile:
        json.dump(Qaria_dati, outfile)


def mediamesi(): #questa funzione ci crea il file con le medie mensili
    media_mensile = {}

    with open("Qaria_dati.json", "r") as file:
        Qaria_dati = json.load(file)

    with open("proprietà_stazioni.json", "r") as file:
        Stazioni = json.load(file)

    stazioni_inquinanti = {}
    for stazione in Stazioni:
        stazione_id = str(list(stazione[0].values())[0])
        inquinanti = stazione[1]["Inquinante"]
        stazioni_inquinanti[stazione_id] = inquinanti
#ciao
    for stazione_id in Qaria_dati.keys():
        media_mensile[stazione_id] = {}
        

        inquinanti_stazione = stazioni_inquinanti.get(stazione_id, [])
        
        for anno in range(2015, 2026):
            media_mensile[stazione_id][anno] = {}
            
            for mese in range(1, 13):
                media_mensile[stazione_id][anno][mese] = {}
                
                for inquinante in inquinanti_stazione:
                    valori = []
                    
                    
                    for data, inquinanti_data in Qaria_dati[stazione_id].items():
                        try:
                            anno_data = int(data.split("-")[0])
                            mese_data = int(data.split("-")[1])
                            
                            if anno_data == anno and mese_data == mese:
                                if inquinante in inquinanti_data:
                                    valore = inquinanti_data[inquinante]
                                    if valore is not None:
                                        try:
                                            valori.append(float(valore))
                                        except (ValueError, TypeError):
                                            pass
                        except (IndexError, ValueError):
                            pass
                    
                    if valori:
                        media_mensile[stazione_id][anno][mese][inquinante] = sum(valori) / len(valori)
                    else:
                        media_mensile[stazione_id][anno][mese][inquinante] = None

    with open("media_mensile.json", "w") as outfile:
        json.dump(media_mensile, outfile, indent=2)


def media_MESI_BELLI():
    with open("media_mensile.json", "r") as file:
        media_mensile = json.load(file)


    media_mensile_pulita = {}

    for stazione_id, anni in media_mensile.items():
        media_mensile_pulita[stazione_id] = {}
        
        for anno, mesi in anni.items():
            media_mensile_pulita[stazione_id][anno] = {}
            
            for mese, inquinanti in mesi.items():
                
                inquinanti_puliti = {
                    inquinante: valore 
                    for inquinante, valore in inquinanti.items() 
                    if valore is not None
                }
                
                if inquinanti_puliti:
                    media_mensile_pulita[stazione_id][anno][mese] = inquinanti_puliti
            
            
            if not media_mensile_pulita[stazione_id][anno]:
                del media_mensile_pulita[stazione_id][anno]


        if not media_mensile_pulita[stazione_id]:
            del media_mensile_pulita[stazione_id]


        with open("media_mensile_pulita.json", "w") as outfile:
            json.dump(media_mensile_pulita, outfile, indent=2)

        print("File media_mensile_pulita.json creato con successo!")
        print("Dati nullati rimossi.")


if __name__ == "__main__":
    stazioni()
    che_inquinanti_ci_sono()
    carica_dati_Qaria()
    mediamesi()
    media_MESI_BELLI

    