import requests
import pandas as pd
import streamlit as st
import datetime

# ---- API URL ----
API_URL = "https://economic-calendar.tradingview.com/events"

# ---- Liste des pays disponibles ----
COUNTRIES = {
    "Afghanistan": "AF", "Albanie": "AL", "Algérie": "DZ", "Andorre": "AD", "Angola": "AO",
    "Antigua-et-Barbuda": "AG", "Arabie Saoudite": "SA", "Argentine": "AR", "Arménie": "AM", 
    "Australie": "AU", "Autriche": "AT", "Azerbaïdjan": "AZ", "Bahamas": "BS", "Bahreïn": "BH", 
    "Bangladesh": "BD", "Barbade": "BB", "Belgique": "BE", "Belize": "BZ", "Bénin": "BJ", 
    "Bermudes": "BM", "Bhoutan": "BT", "Bolivie": "BO", "Bosnie-Herzégovine": "BA", "Botswana": "BW", 
    "Brésil": "BR", "Brunei Darussalam": "BN", "Bulgarie": "BG", "Burkina Faso": "BF", "Burundi": "BI", 
    "Cambodge": "KH", "Cameroun": "CM", "Canada": "CA", "Cap-Vert": "CV", "Chili": "CL", 
    "Chine": "CN", "Chypre": "CY", "Colombie": "CO", "Comores": "KM", "Congo": "CG", 
    "Congo (Rép. dém. du)": "CD", "Corée du Nord": "KP", "Corée du Sud": "KR", "Costa Rica": "CR", 
    "Croatie": "HR", "Cuba": "CU", "Danemark": "DK", "Djibouti": "DJ", "Dominique": "DM", 
    "Égypte": "EG", "El Salvador": "SV", "Émirats Arabes Unis": "AE", "Équateur": "EC", "Érythrée": "ER", 
    "Espagne": "ES", "Estonie": "EE", "États-Unis": "US", "Éthiopie": "ET", "Fidji": "FJ", 
    "Finlande": "FI", "France": "FR", "Gabon": "GA", "Gambie": "GM", "Géorgie": "GE", 
    "Ghana": "GH", "Gibraltar": "GI", "Grèce": "GR", "Grenade": "GD", "Guatemala": "GT", 
    "Guinée": "GN", "Guinée-Bissau": "GW", "Guyana": "GY", "Haïti": "HT", "Honduras": "HN", 
    "Hong Kong": "HK", "Hongrie": "HU", "Inde": "IN", "Indonésie": "ID", "Irak": "IQ", 
    "Irlande": "IE", "Islande": "IS", "Israël": "IL", "Italie": "IT", "Jamaïque": "JM", 
    "Japon": "JP", "Jordanie": "JO", "Kazakhstan": "KZ", "Kenya": "KE", "Kirghizistan": "KG", 
    "Kiribati": "KI", "Koweït": "KW", "Laos": "LA", "Lesotho": "LS", "Lettonie": "LV", 
    "Liban": "LB", "Liberia": "LR", "Libye": "LY", "Liechtenstein": "LI", "Lituanie": "LT", 
    "Luxembourg": "LU", "Macédoine du Nord": "MK", "Madagascar": "MG", "Malaisie": "MY", "Malawi": "MW", 
    "Maldives": "MV", "Mali": "ML", "Malte": "MT", "Maroc": "MA", "Marshall (îles)": "MH", 
    "Maurice": "MU", "Mauritanie": "MR", "Mexique": "MX", "Micronésie": "FM", "Moldavie": "MD", 
    "Monaco": "MC", "Mongolie": "MN", "Monténégro": "ME", "Mozambique": "MZ", "Namibie": "NA", 
    "Nauru": "NR", "Népal": "NP", "Nicaragua": "NI", "Niger": "NE", "Nigéria": "NG", 
    "Niue": "NU", "Norvège": "NO", "Nouvelle-Zélande": "NZ", "Oman": "OM", "Ouganda": "UG", 
    "Pakistan": "PK", "Palaos": "PW", "Panama": "PA", "Papouasie-Nouvelle-Guinée": "PG", "Paraguay": "PY", 
    "Pays-Bas": "NL", "Pérou": "PE", "Philippines": "PH", "Pologne": "PL", "Portugal": "PT", 
    "Qatar": "QA", "République Dominicaine": "DO", "République tchèque": "CZ", "Roumanie": "RO", 
    "Royaume-Uni": "GB", "Russie": "RU", "Rwanda": "RW", "Saint-Kitts-et-Nevis": "KN", "Saint-Vincent-et-les-Grenadines": "VC", 
    "Sainte-Lucie": "LC", "Salvador": "SV", "Samoa": "WS", "Sao Tomé-et-Principe": "ST", "Sénégal": "SN", 
    "Serbie": "RS", "Seychelles": "SC", "Sierra Leone": "SL", "Singapour": "SG", "Soudan": "SD", 
    "Sri Lanka": "LK", "Syrie": "SY", "Tadjikistan": "TJ", "Tanzanie": "TZ", "Tchad": "TD", 
    "Thaïlande": "TH", "Timor oriental": "TL", "Togo": "TG", "Trinité-et-Tobago": "TT", "Tunisie": "TN", 
    "Turkménistan": "TM", "Turquie": "TR", "Tuvalu": "TV", "Ukraine": "UA", "Uruguay": "UY", 
    "Vanuatu": "VU", "Vatican": "VA", "Venezuela": "VE", "Viêt Nam": "VN", "Yémen": "YE", "Zambie": "ZM", 
    "Zimbabwe": "ZW","UE": "EU"
}

# ---- Dictionnaire des niveaux d'importance ----
IMPORTANCE_MAP = {
    -1: "Faible",
    0: "Moyenne",
    1: "Haute"
}

def get_economic_calendar(start_date, countries_selected):
    """Récupère les événements économiques entre une date donnée et +7 jours"""
    

    # Convertir start_date et end_date en objets datetime pour ajouter l'heure
    start_datetime = datetime.datetime.combine(start_date, datetime.time(0, 0, 0))  # Heure 00:00:00
    end_datetime = datetime.datetime.combine(start_date, datetime.time(23, 59, 59))  # Heure 23:59:59

    


    # Format ISO pour l'API
    start_date_iso = start_datetime.isoformat() + ".000Z"
    end_date_iso = end_datetime.isoformat() + ".000Z"

    payload = {
        "from": start_date_iso,
        "to": end_date_iso,
       # "countries": ",".join(countries_selected),
    }

    headers = {
        "Origin": "https://in.tradingview.com"
    }

    response = requests.post(API_URL, headers=headers, params=payload)

    if response.status_code == 200:
        data = response.json()
        
        #st.write("Réponse API brute :", data)  # DEBUG
        
        # Vérification de la structure de la réponse
        if isinstance(data, dict) and "result" in data:
            df = pd.DataFrame(data['result'])
            return df.assign(
                date=lambda df: pd.to_datetime(df['date'])+pd.DateOffset(hours=1),
                country=lambda df: df['country'].astype("str"),
                count=lambda df: (df["date"]).dt.time,  # Extract hour
            )
        else:
            st.error("Format de réponse API non valide.")
            return []
    else:
        st.error(f"Erreur API ({response.status_code}): {response.text}")
        return None

# ---- Streamlit UI ----
st.title("📅 Calendrier Économique - TradingView")

# ✅ Sélection de la date
selected_date = st.date_input("📅 Date de début :", datetime.date.today())

# # ✅ Sélection des pays
# selected_countries = st.sidebar.multiselect(
#     "🌍 Pays :", list(COUNTRIES.keys()), default=["États-Unis"]
# )
selected_countries = ["États-Unis"]
# ✅ Filtrer par importance (afficher seulement les événements importants)
only_important = st.checkbox("Afficher uniquement les événements importants", value=True)


country_codes = [COUNTRIES[c] for c in selected_countries]  # Convertir en code API
events = get_economic_calendar(selected_date, country_codes)

if events is not None and not events.empty:
    df = pd.DataFrame(events)

    # ✅ Sélectionner les colonnes pertinentes et ajouter l'importance
    df = df[["count", "country","indicator", "actual", "forecast", "previous", "importance"]]

    # ✅ Mapper les codes pays en noms
    reverse_country_map = {v: k for k, v in COUNTRIES.items()}
    df["country"] = df["country"].map(reverse_country_map)

    # ✅ Mapper l'importance à partir du dictionnaire
    df["importance"] = df["importance"].map(IMPORTANCE_MAP)

    if only_important:
        df = df[df["importance"] == "Haute"]

    st.subheader(f"📊 Événements économiques du {selected_date} +7 jours")
    st.dataframe(df,hide_index=True)
else:
    st.warning("⚠️ Aucun événement trouvé pour cette période et ces pays.")
