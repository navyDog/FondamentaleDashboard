import streamlit as st
import requests
import pandas as pd






# ---- API URL ----
API_URL = "https://publicreporting.cftc.gov/resource/6dca-aqww.json"

# ---- Codes des marchés Forex ----
FOREX_MARKETS = {
    "USD": "USD INDEX - ICE FUTURES U.S.",
    "JPY": "JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE",
    "AUD": "AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE",
    "nasdaq": "NASDAQ-100 Consolidated - CHICAGO MERCANTILE EXCHANGE",
    "dow": "DOW JONES U.S. REAL ESTATE IDX - CHICAGO BOARD OF TRADE",
    "oil": "WTI CRUDE OIL 1ST LINE - ICE FUTURES ENERGY DIV",
    "gas": "WTI CRUDE OIL 1ST LINE - ICE FUTURES ENERGY DIV",
    "eur": "EURO FX - CHICAGO MERCANTILE EXCHANGE",
    "gold": "GOLD - COMMODITY EXCHANGE INC.",
    "CAD": "CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE",
    "BTC": "BITCOIN - CHICAGO MERCANTILE EXCHANGE",
    "ETH": "MICRO ETHER - CHICAGO MERCANTILE EXCHANGE",
    "silver": "SILVER - COMMODITY EXCHANGE INC.",
    "NZD": "NZ DOLLAR - CHICAGO MERCANTILE EXCHANGE",
    "CHF": "SWISS FRANC - CHICAGO MERCANTILE EXCHANGE",
    "GBP": "BRITISH POUND - CHICAGO MERCANTILE EXCHANGE",
    "S&P500": "S&P 500 Consolidated - CHICAGO MERCANTILE EXCHANGE",
}

def get_available_dates():
    """Récupère toutes les dates disponibles depuis l'API"""
    params = {"$select": "distinct report_date_as_yyyy_mm_dd", "$order": "report_date_as_yyyy_mm_dd DESC"}
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        dates = [item["report_date_as_yyyy_mm_dd"] for item in response.json()]
        return sorted(pd.to_datetime(dates), reverse=True)
    else:
        st.error(f"Erreur API ({response.status_code}): {response.text}")
        return []

def get_all_market_names():
    """Récupère et affiche la liste de tous les noms de marché disponibles"""
    params = {
        "$limit": 5000 # Limiter à 5000 résultats pour obtenir un échantillon large
    }
    
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if not data:
            print("Aucune donnée reçue")
            return []
        
        # Convertir en DataFrame pour une manipulation facile
        df = pd.DataFrame(data)
        
        # Vérifier les colonnes disponibles
        if "market_and_exchange_names" in df.columns:
            # Extraire les valeurs uniques de cette colonne
            market_names = df["market_and_exchange_names"].unique()
            return market_names
        else:
            print("La colonne 'market_and_exchange_names' n'existe pas dans les données.")
            return []
    else:
        print(f"Erreur API ({response.status_code}): {response.text}")
        return []


def get_cot_data(selected_markets, selected_date):
    """Récupère les données COT pour la date et les marchés sélectionnés"""
    if not selected_markets or not selected_date:
        return None

    where_clause = " OR ".join([f"market_and_exchange_names='{FOREX_MARKETS[m]}'" for m in selected_markets])

    params = {
        "$where": f"({where_clause}) AND report_date_as_yyyy_mm_dd <= '{selected_date.date()}'",
        "$order": "report_date_as_yyyy_mm_dd DESC",
        "$limit": 100
    }

    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if not data:
            st.error("Aucune donnée trouvée.")
            return None
        
        df = pd.DataFrame(data)

        # ✅ Conversion de la colonne date
        df["report_date_as_yyyy_mm_dd"] = pd.to_datetime(df["report_date_as_yyyy_mm_dd"])

        # ✅ Sélection des deux dernières dates disponibles pour la comparaison
        latest_dates = df["report_date_as_yyyy_mm_dd"].unique()[:2]  

        # ✅ Filtrage des deux dernières dates
        df = df[df["report_date_as_yyyy_mm_dd"].isin(latest_dates)]

        return df
    else:
        st.error(f"Erreur API ({response.status_code}): {response.text}")
        return None


def get_latest_cot_data(selected_markets):
    """Récupère les dernières données COT pour tous les marchés Forex en une seule requête"""
    if not selected_markets:
        return None  # Si aucun marché n'est sélectionné

    where_clause = " OR ".join([f"market_and_exchange_names='{FOREX_MARKETS[m]}'" for m in selected_markets])


    params = {
        "$where": where_clause,
        "$order": "report_date_as_yyyy_mm_dd DESC",
        "$limit": 100
    }

    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if not data:
            st.error("Aucune donnée trouvée.")
            return None
        df = pd.DataFrame(data)

        # ✅ Conversion de la colonne date
        df["report_date_as_yyyy_mm_dd"] = pd.to_datetime(df["report_date_as_yyyy_mm_dd"])

        # ✅ Sélection des deux dernières dates disponibles
        latest_dates = df["report_date_as_yyyy_mm_dd"].unique()[:2]  

        # ✅ Filtrage des deux dernières dates
        df = df[df["report_date_as_yyyy_mm_dd"].isin(latest_dates)]

        return df
    else:
        st.error(f"Erreur API ({response.status_code}): {response.text}")
        return None

# def get_cot_data(market_name):
#     """Récupère les données COT via l'API avec le bon filtre"""
#     params = {
#         "market_and_exchange_names": market_name,  # Utiliser le bon champ
#          "$limit": 2,  # On ne récupère que les 4 dernières entrées
#         "$order": "report_date_as_yyyy_mm_dd DESC"
#     }
    
#     response = requests.get(API_URL, params=params)

#     if response.status_code == 200:
#         data = response.json()
#         if not data:
#             st.error("Aucune donnée trouvée pour ce marché.")
#             return None
#         return pd.DataFrame(data)
#     else:
#         st.error(f"Erreur API ({response.status_code}): {response.text}")
#         return None


st.title("📊 COT Report - Legacy")
st.header("Sélection des marchés & Date")

# Multi-select pour choisir les marchés à afficher
selected_markets = st.multiselect(
    "Sélectionnez les marchés Forex :", 
    options=list(FOREX_MARKETS.keys()), 
    default=list(FOREX_MARKETS.keys())  # Par défaut, tous les marchés sont sélectionnés
)


# ✅ Récupération des dates disponibles
available_dates = get_available_dates()
selected_date = st.selectbox("Choisissez une date :", available_dates)




# Sélection du marché Forex
# market_name = st.sidebar.selectbox("Sélectionnez un marché :", list(get_all_market_names()))
# market_code = market_name

# market_name = st.selectbox("Sélectionnez une devise :", list(FOREX_MARKETS.keys()))
# market_code = FOREX_MARKETS[market_name]  # Nom attendu par l'API

# Chargement des données

#df = get_latest_cot_data(selected_markets)

# ✅ Récupération des données
df = get_cot_data(selected_markets, selected_date)
#a =st.write(f"🔄 Chargement des données pour **{selected_markets}**...")
if df is not None and not df.empty:
   # a=st.empty()

    # ✅ Conversion des colonnes numériques
    numeric_cols = ["noncomm_positions_long_all", "noncomm_positions_short_all", 
                    "comm_positions_long_all", "comm_positions_short_all"]
    
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

     # ✅ Tri des données par marché et date décroissante
    df = df.sort_values(by=["market_and_exchange_names", "report_date_as_yyyy_mm_dd"], ascending=[True, False])

      # ✅ Création des colonnes de variation
    df["Variation Longs"] = df.groupby("market_and_exchange_names")["noncomm_positions_long_all"].diff(-1)
    df["Variation Shorts"] = df.groupby("market_and_exchange_names")["noncomm_positions_short_all"].diff(-1)

    # ✅ Sélection des colonnes utiles
    df_filtered = df[["report_date_as_yyyy_mm_dd", "market_and_exchange_names", 
                       "noncomm_positions_long_all", "noncomm_positions_short_all", 
                       "comm_positions_long_all", "comm_positions_short_all",
                        "Variation Longs", "Variation Shorts"]]
    
    # ✅ Renommage des colonnes pour affichage
    df_filtered = df_filtered.rename(columns={
        "report_date_as_yyyy_mm_dd": "Date",
        "market_and_exchange_names": "Marché",
        "noncomm_positions_long_all": "Longs Non-Commerciaux",
        "noncomm_positions_short_all": "Shorts Non-Commerciaux",
        "comm_positions_long_all": "Longs Commerciaux",
        "comm_positions_short_all": "Shorts Commerciaux",
    })
    print (df_filtered)

    # ✅ Remplacement des noms API par des noms lisibles
    df_filtered["Marché"] = df_filtered["Marché"].replace({v: k for k, v in FOREX_MARKETS.items()})

     # ✅ Filtrage pour n'afficher que la dernière date (et la variation par rapport à l'avant-dernière)
    latest_date = df_filtered["Date"].max()
    df_filtered = df_filtered[df_filtered["Date"] == latest_date]
    



    # ✅ Affichage du tableau trié par marché
    df_filtered = df_filtered.sort_values(by="Marché")

    st.subheader(f"📅 Données du {df_filtered['Date'].iloc[0].date()}")
    
    
    st.data_editor(
        df_filtered,
        column_config={
            "Date": st.column_config.DatetimeColumn(
            "Date",
            format="D MMM YYYY",
            step=60,
        ),
        },
        hide_index=True,
    )
    

else:
    st.warning("Sélectionnez au moins un marché pour voir les données.")





    # left_col, middle_col, right_col = st.columns(3)

    # with left_col:
    #     st.metric(
    #         label=market_name,
    #         valueLong=f"$ {df_filtered["Variation Longs"]:,.2f}",
    #         valueShort=f"$ {df_filtered["Variation Short"]:,.2f}",
    #         deltaLong=f"{df_filtered["Variation Longs"], 'change']:.2f}% vs. Last Report",
    #         deltaShort=f"{df_filtered["Variation Shorts"], 'change']:.2f}% vs. Last Report",
    # )
    # a=(df_filtered["Variation Longs"])[0]
    # with left_col:
    #     st.metric(
    #         label= " Long non commerciaux",
    #         value=(df_filtered["Longs Non-Commerciaux"]).tolist()[1],
    #         # valueShort=df_filtered["Shorts Non-Commerciaux"],
    #         #delta=(df_filtered["Variation Longs"])[0]
    #         delta=f"{a} vs. Last Report",
    #         # deltaShort=f"{df_filtered["Variation Shorts"], 'change':.2f}% vs. Last Report",
    # )
        
    # b=(df_filtered["Variation Shorts"])[0]
    # with left_col:
    #     st.metric(
    #         label= " Shorts non commerciaux",
    #         value=(df_filtered["Shorts Non-Commerciaux"]).tolist()[1],
    #         # valueShort=df_filtered["Shorts Non-Commerciaux"],
    #         #delta=(df_filtered["Variation Longs"])[0]
    #         delta=f"{b} vs. Last Report",
    #         # deltaShort=f"{df_filtered["Variation Shorts"], 'change':.2f}% vs. Last Report",
    # )

# data_df = pd.DataFrame(
#     {
#         "appointment": [
#             datetime(2024, 2, 5, 12, 30),
#             datetime(2023, 11, 10, 18, 0),
#             datetime(2024, 3, 11, 20, 10),
#             datetime(2023, 9, 12, 3, 0),
#         ]
#     }
# )

# st.data_editor(
#     data_df,
#     column_config={
#         "appointment": st.column_config.DatetimeColumn(
#             "Appointment",
#             min_value=datetime(2023, 6, 1),
#             max_value=datetime(2025, 1, 1),
#             format="D MMM YYYY, h:mm a",
#             step=60,
#         ),
#     },
#     hide_index=True,
# )




    # ---- Affichage d'un graphique ----
    # st.subheader("📈 Évolution des positions Non-Commerciaux")
    # fig, ax = plt.subplots(figsize=(10, 5))
    # ax.plot(df_filtered["Date"], df_filtered["Longs Non-Commerciaux"], label="Longs", color="green")
    # ax.plot(df_filtered["Date"], df_filtered["Shorts Non-Commerciaux"], label="Shorts", color="red")
    # ax.set_xlabel("Date")
    # ax.set_ylabel("Positions")
    # ax.set_title(f"Évolution des Positions COT - {market_name}")
    # ax.legend()
    # ax.grid()
    # st.pyplot(fig)
