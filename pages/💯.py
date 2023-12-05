import os
import json
import streamlit as st

def load_json_objects(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            json_strings = file.read().split('\n')
        return [json.loads(js) for js in json_strings if js.strip()]
    except Exception as e:
        print(f"Error loading JSON objects: {e}")
        return []

def generate_workstation_json_files(orders):
    common_fields = ['Bestelldatum und Uhrzeit', 'Kunde', 'Auftragsnummer', 'Sonderwunsch', 'Kundentakt']
    specific_fields = {
        "Rädermontage": {"Achse": 5, "Reifen": 10},
        "Montage Führerhaus": {},
        "Auflieger-Fahrgestell": {"Achse": 3, "Reifen": 6},
        "Montage Auflieger": {},
        "Montage Zugmaschine": {"Achse": 2, "Reifen": 4},
        "Endmontage": {}
    }

    varianten_fields = {
        "Montage Führerhaus": ["Führerhaus", "Sidepipes"],
        "Montage Auflieger": ["Container 1", "Container 2", "Container 3", "Container 4"]
    }

    workstation_orders = {task: [] for task in specific_fields}
    for order in orders:
        for task, fields in specific_fields.items():
            order_info = {field: order[field] for field in common_fields}
            order_info.update(fields)

            if task in varianten_fields:
                varianten = order.get('Variante nach Bestellung', {})
                for field in varianten_fields[task]:
                    order_info[field] = varianten.get(field, 'N/A')

            workstation_orders[task].append(order_info)

    output_directory = 'pages'
    for task, orders in workstation_orders.items():
        filename = f"{task.replace(' ', '_')}.json"
        full_path = os.path.join(output_directory, filename)
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(orders, f, ensure_ascii=False, indent=4)
        print(f"File written: {full_path}")

    st.success("Alle JSON-Dateien wurden erfolgreich erstellt.")

file_path = 'bestellungen_database.json'
if os.path.exists(file_path):
    orders = load_json_objects(file_path)
    if orders:
        generate_workstation_json_files(orders)
    else:
        st.warning("Keine Bestellungen zum Verarbeiten gefunden.")
else:
    st.error(f"Datei nicht gefunden: {file_path}")