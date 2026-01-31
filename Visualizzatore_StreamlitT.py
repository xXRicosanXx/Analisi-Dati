import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go


st.set_page_config(page_title="Visualizzatore 3000!", layout="wide")


st.title("Visualizza I dati CON: VISUALIZATORE 3000!")


with open("media_mensile_pulita.json", "r") as file:
    media_mensile = json.load(file)


st.sidebar.header("Menu Principale")


visualizzazione = st.sidebar.radio(
    "Seleziona Visualizzazione:",
    ["📊 Media Mensile", "ℹ️ Informazioni Inquinanti"]
)

st.sidebar.divider()
st.sidebar.header("Seleziona i parametri") 

stazioni = sorted(list(media_mensile.keys()), key=lambda x: int(x))
stazione_selezionata = st.sidebar.selectbox(
    "Seleziona Stazione:",
    stazioni,
    format_func=lambda x: f"Stazione {x}"
)


anni_disponibili = sorted([int(anno) for anno in media_mensile[stazione_selezionata].keys()])
anni_selezionati = st.sidebar.multiselect(
    "Seleziona Anni:",
    anni_disponibili,
    default=anni_disponibili
)


inquinanti_disponibili = set()
mesi_disponibili = set()

for anno in anni_selezionati:
    for mese, inquinanti in media_mensile[stazione_selezionata][str(anno)].items():
        mesi_disponibili.add(int(mese))
        inquinanti_disponibili.update(inquinanti.keys())

inquinanti_disponibili = sorted(list(inquinanti_disponibili))
mesi_disponibili = sorted(list(mesi_disponibili))


inquinanti_selezionati = st.sidebar.multiselect(
    "Seleziona Inquinanti:",
    inquinanti_disponibili,
    default=inquinanti_disponibili
)


mesi_selezionati = st.sidebar.multiselect(
    "Seleziona Mesi:",
    mesi_disponibili,
    default=mesi_disponibili
)


if visualizzazione == "📊 Media Mensile":
    dati_grafico = []

    for anno in anni_selezionati:
        for mese in mesi_selezionati:
            if str(mese) in media_mensile[stazione_selezionata][str(anno)]:
                mese_data = media_mensile[stazione_selezionata][str(anno)][str(mese)]
                
                for inquinante in inquinanti_selezionati:
                    if inquinante in mese_data:
                        valore = mese_data[inquinante]
                        data_str = f"{anno}-{mese:02d}"
                        dati_grafico.append({
                            "Data": data_str,
                            "Anno": anno,
                            "Mese": mese,
                            "Inquinante": inquinante,
                            "Valore": valore
                        })

    if dati_grafico:
        df = pd.DataFrame(dati_grafico)
        
        st.header("📊 Media Mensile")
        
        fig = go.Figure()
        
        for inquinante in inquinanti_selezionati:
            df_inquinante = df[df['Inquinante'] == inquinante]
            if not df_inquinante.empty:
                fig.add_trace(go.Scatter(
                    x=df_inquinante['Data'],
                    y=df_inquinante['Valore'],
                    mode='lines+markers',
                    name=inquinante
                ))
        
        fig.update_layout(
            title=f"Valori Medi Mensili - Stazione {stazione_selezionata}",
            xaxis_title="Data",
            yaxis_title="Valore",
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        

        st.header("Tabella Dati")
        st.dataframe(
            df.pivot_table(
                values='Valore',
                index='Data',
                columns='Inquinante',
                aggfunc='first'
            ),
            use_container_width=True
        )
        
    else:
        st.warning("Nessun dato disponibile con i parametri selezionati")

elif visualizzazione == "ℹ️ Informazioni Inquinanti":
    st.header("ℹ️ Informazioni Inquinanti")
    
    inquinanti_info = {
        "PM10": {
            "descrizione": "Particolato Fine (10 micrometri)",
            "limite": "50 µg/m³ (medio giornaliero)",
            "effetti": "Irritazione delle vie respiratorie, malattie polmonari croniche"
        },
        "PM2.5": {
            "descrizione": "Particolato Ultra-fine (2.5 micrometri)",
            "limite": "25 µg/m³ (medio annuale)",
            "effetti": "Penetra nei polmoni, effetti cardiovascolari e respiratori"
        },
        "NO2": {
            "descrizione": "Biossido di Azoto",
            "limite": "200 µg/m³ (orario)",
            "effetti": "Irritazione delle vie respiratorie, aumenta suscettibilità alle infezioni"
        },
        "O3": {
            "descrizione": "Ozono (al livello del suolo)",
            "limite": "120 µg/m³ (medio su 8 ore)",
            "effetti": "Riduce la funzione polmonare, asma, allergie respiratorie"
        },
        "SO2": {
            "descrizione": "Biossido di Zolfo",
            "limite": "350 µg/m³ (orario)",
            "effetti": "Irritazione respiratoria, effetti cardiovascolari"
        },
        "CO": {
            "descrizione": "Monossido di Carbonio",
            "limite": "10 mg/m³ (media su 8 ore)",
            "effetti": "Riduce il trasporto di ossigeno nel sangue"
        }
    }
    
    for inquinante, info in inquinanti_info.items():
        with st.expander(f"🔬 {inquinante}"):
            st.write(f"**Descrizione:** {info['descrizione']}")
            st.write(f"**Limite normativo:** {info['limite']}")
            st.write(f"**Effetti sulla salute:** {info['effetti']}")
