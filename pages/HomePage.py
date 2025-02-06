import streamlit as st

from forms.contact import contact_form

@st.dialog("Contact Me")
def show_contact_form():
    contact_form()


# --- HERO SECTION ---

col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.image("assets/7.jpg", width=230)
with col2:
    st.title("Données pour l'analyse Fondamentale", anchor=False)
    st.write(
        "retrouvez un outil simple d'utilisation qui regroupe un maximum de données pour pratiquer l'analyse Fondamentale. Work in Porgress..."
    )
    if st.button("Contactez nous"):
        show_contact_form()



# --- Calendrier Economique --- 
st.write("\n")
st.subheader("Calendrier Economique", anchor=False)
st.write(
    """
    -Acces aux info eco blabla \n
    -blavbla \n
    -Tri des données
    """
)