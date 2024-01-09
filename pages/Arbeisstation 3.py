import os
import streamlit as st
import json
from datetime import datetime
from utils import display_order_info

# 定义 selections.json 文件的路径
selections_file_path = r'C:\Users\zxm14\Documents\GitHub\Montagesimulation\pages\selections.json'

def load_json_data(filename):
    """加载 JSON 文件"""
    if os.path.exists(filename):
        with open(filename, "r", encoding='utf-8') as file:
            return json.load(file)
    else:
        return None

def save_duration_data(data, filename):
    """保存持续时间数据到指定的 JSON 文件"""
    with open(filename, "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def main():
    station_number = '3'  # 每个 Arbeitsstation 文件中设置不同的编号
    
    # 从 selections.json 文件读取选定的工作流程
    selections = load_json_data(selections_file_path)
    selected_workflow = selections.get(f"Arbeitsstation{station_number}_workflow", None)

    if selected_workflow:
        st.header(f"Arbeitsstation {station_number}: {selected_workflow}")

        json_file = os.path.join('pages', f"{selected_workflow.replace(' ', '_')}.json")
        data = load_json_data(json_file)

        if data is not None:
            duration_data_key = f'duration_data_{station_number}'  # 使用唯一的键
            if duration_data_key not in st.session_state:
                st.session_state[duration_data_key] = []

            for i, order in enumerate(data, start=1):
                with st.expander(f"Order {i}"):
                    display_order_info(order)

                    col1, col2 = st.columns(2)
                    start_button = col1.button(f"Starten Order {i}", key=f"start_{station_number}_{i}")
                    end_button = col2.button(f"Beenden Order {i}", key=f"end_{station_number}_{i}")

                    if start_button:
                        st.session_state[f'start_time_{station_number}_{i}'] = datetime.now()
                    if end_button and f'start_time_{station_number}_{i}' in st.session_state:
                        end_time = datetime.now()
                        duration = int((end_time - st.session_state[f'start_time_{station_number}_{i}']).total_seconds())
                        st.session_state[duration_data_key].append({"Order": i, "Dauerzeit": duration, "Kundentakt": order.get("Kundentakt")})

            # 显示每个订单的 Dauerzeit
            for item in st.session_state[duration_data_key]:
                st.markdown(f"Dauerzeit für Order {item['Order']}: <span style='color: red;'>{item['Dauerzeit']} Sekunden</span>", unsafe_allow_html=True)

            # 保存持续时间数据到 JSON 文件
            if st.button("Daten speichern"):
                save_duration_file = os.path.join('pages', f'Arbeitsstation{station_number}_durations.json')
                save_duration_data(st.session_state[duration_data_key], save_duration_file)
                st.success("Daten erfolgreich gespeichert!")

        else:
            st.error(f"Datei nicht gefunden: {json_file}")
    else:
        st.error("Kein Workflow ausgewählt für Arbeitsstation {station_number}.")

if __name__ == "__main__":
    main()
