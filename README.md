In questa attività abbiamo analizziato i dati di 9 stazioni situate a milano, ciascuna di esse analliza varie inquinanti: ['NO2', 'SO2', 'O3', 'PM10', 'C6H6', 'PM25', 'CO_8h'].
I dati a disposizione vanno dal 2015 al 2025, nel corso di questa attività i dati visuallizatti nei file json, tramite Visualizzatore3000.py, abbiamo notato una distribuzione 
disomogena relativa al tempo di lavoro e questo comporta ad un analisi parziale dei 10 anni.

All'interno di ogni stazione, con il corrispettivo station id, è presente la data di inizio e fine riguardante l'operabilità, ciò si può visualizzare nel file Stazioni.json. 
Nelle stazione ancora attive è presente la data "2099-12-31T00:00:00" e tutte iniziano la loro oreratività nell "1900-01-01T00:00:00", in realtà è solo una data fasulla data
dall'orologio interno dei computer, per le restanti la loro operatività finisce prima come per la stazione 1 nel "2017-08-31T00:00:00". 

infatti la stazione 9 ha finito la sua operatività nel 2007 e questo comporta la sua assenza nei grafici.

per la documentazione della librera streamlit abbiamo utilizato il sito ufficiale: https://docs.streamlit.io/develop

con il file Visualizatore3000.py analiziamo tutti i file json e in putput ci ritorna un file Qaria dove sono presenti tutti i dati divisi per stazione (il suo id) e in ognuno ogni giorno e cosa ha analizato.
e anche media menisle che però va pulità poichè crea mesi in cui non sono presenti dati cioò comporta la presenza di molti dati null
 
