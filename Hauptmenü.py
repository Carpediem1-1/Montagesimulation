#test
# Contents of ~/my_app/main_page.py
import streamlit as st


st.sidebar.image("https://www.fau.de/files/2021/10/neues-fau-logo-nur-fuer-webmeldung-1024x198.jpg", use_column_width=True)

st.markdown("# Hauptmenü 🏚️")
st.sidebar.markdown("# Hauptmenü 🏚️")

st.title("Montagesimulation")
st.write("Im Rahmen eines Praktikums wird die Analyse und Optimierung nach Methoden der schlanken Produktion vermittelt.")
st.write("Diese Streamlit App dient der digitalen Abbildung von Bestellungen, deren Bearbeitung und Qualitätskontrolle")


col1, col2 = st.columns(2)

with col1:
   #st.header("Montagelayout")
   #st.image("layout.JPG",width=300)

with col2:
   #st.header("Link zum Tool")
   #st.image("QR.jpg",width=240)
