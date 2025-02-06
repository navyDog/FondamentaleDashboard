import streamlit as st




hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
# --- CONFIGURATION DES PAGES ---

home_page = st.Page(
    page = "pages/HomePage.py",
    title = "HomePage",
    icon = ":material/home:",
    default = True,
)

calendar_page = st.Page(
    page = "pages/Economic_calendar.py",
    title = "Calendrier Economique",
    icon = ":material/calendar_month:",
)

cot_page = st.Page(
    page = "pages/COT_Data.py",
    title = "COT Report",
    icon = ":material/partner_reports:"
)

# --- MENU DE NAVIGUATION ---
pg = st.navigation(
    {
        "" : [home_page],
        "Data" : [calendar_page, cot_page],
        
    })
# --- CONFIG DE BASE --- 

st.logo("assets/7.jpg")
st.sidebar.text("Made by JC for all")


# --- RUN NAV ---
pg.run()