import streamlit as st
import datetime
import json

# 使用Streamlit的session状态来跟踪提交状态
if 'submit_clicked' not in st.session_state:
    st.session_state['submit_clicked'] = False

st.markdown("# Bestellen 🏪")
st.sidebar.markdown("# Bestellen 🏪")

# Datenbank-Datei für Werkzeugnisinformationen im JSON-Format
database_filename = "bestellungen_database.json"

# Laden der bestehenden Werkzeugnisdaten aus der JSON-Datei
def load_existing_data(filename):
    try:
        with open(filename, "r") as file:
            data = [json.loads(line) for line in file]
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []

existing_data = load_existing_data(database_filename)

# Kunde
kunde = st.text_input("Kundenname")

# Automatisches Einfügen des aktuellen Datums und der Uhrzeit
current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Generiere die Auftragsnummer aus den ersten Buchstaben des Kunden und dem Datum
if kunde:
    auftragsnummer = kunde[:3].upper() + current_datetime.replace("-", "").replace(" ", "").replace(":", "")
    st.write(f"Auftragsnummer: {auftragsnummer}")

st.write(f"Bestellung vom: {current_datetime}")

# Auswahl der Bestellvarianten
st.write("Wählen Sie Ihre Farben aus:")

varianten_farben = {
    "Führerhaus": ["Blau", "Rot", "Gelb"],
    "Sidepipes": ["Rot", "Blau"],
    "Container 1": ["Grün", "Gelb", "Blau"],
    "Container 2": ["Grün", "Gelb", "Blau"],
    "Container 3": ["Grün", "Gelb", "Blau"],
    "Container 4": ["Grün", "Gelb", "Blau"]
}

# Erstelle die Liste von Farben basierend auf gemeinsamen Farben
common_colors_order = {"Blau", "Rot", "Gelb", "Grün"}

# Sortieren Sie die Farben nach der vordefinierten Reihenfolge und alphabetisch für nicht aufgeführte Farben
sorted_colors = {
    variante: sorted(farben, key=lambda color: (color not in common_colors_order, color))
    for variante, farben in varianten_farben.items()
}

selected_variants = {}

# Erstellen von Spalten für die Farbvarianten
columns = st.columns(len(sorted_colors))

# Zeigen Sie die Farben für jede Variante in ihrer eigenen Spalte
for col, (variante, farben) in zip(columns, sorted_colors.items()):
    with col: 
        selected_color = st.radio(f"{variante}", farben, key=f"{variante}")
        if selected_color: 
            selected_variants[variante] = selected_color

# Sonderwunsch
sonderwunsch = st.text_input("Sonderwunsch", "")

# Kundentakt
Kundentakt = st.text_input("Kundentakt", "")

# Schaltfläche, um Bestellung abzuschicken
if st.button("Bestellung abschicken") and not st.session_state['submit_clicked']:
    st.session_state['submit_clicked'] = True  # Update state to clicked
    
    bestellungen_info = {
        "Bestelldatum und Uhrzeit": current_datetime,
        "Kunde": kunde,
        "Auftragsnummer": auftragsnummer,
        "Sonderwunsch": sonderwunsch,
        "Variante nach Bestellung": selected_variants,
        "Kundentakt": Kundentakt,
    }
    existing_data.append(bestellungen_info)  # Add the new data to the existing data

    # Speichern Sie die Daten im JSON-Format in der Datei
    with open(database_filename, "w") as db:
        for entry in existing_data:
            db.write(json.dumps(entry) + "\n")  # Save order information as JSON

    st.write("Die Bestellung wurde abgeschickt.")
    # Nach dem Senden der Bestellung die Möglichkeit bieten, das Formular zurückzusetzen
    st.button("Neue Bestellung", on_click=lambda: st.session_state.update(submit_clicked=False))

elif st.session_state['submit_clicked']:
    # Wenn eine Bestellung bereits abgeschickt wurde, zeigen Sie eine Bestätigung an
    st.success("Ihre Bestellung wurde bereits gesendet. Bitte schicken Sie eine neue Bestellung ab oder aktualisieren Sie die Seite.")