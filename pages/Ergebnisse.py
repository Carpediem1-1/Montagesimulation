import streamlit as st
import matplotlib.pyplot as plt
import json
import os

# Function to load JSON data
def load_json_data(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding='utf-8') as file:
            return json.load(file)
    else:
        return []
# 假设的加载 JSON 数据的函数
def create_chart(order_id, stations_data):
    fig, ax = plt.subplots(figsize=(10, 6))
    stations = [f'Arbeitsstation{i}' for i in range(1, 7)]
    durations = []
    kundentakts = []
    
    # Collecting data for the specified order
    for station in stations:
        station_data = stations_data.get(station, [])
        for data in station_data:
            if str(data['Order']) == str(order_id):
                try:
                    durations.append(int(data['Dauerzeit']))
                    kundentakts.append(int(data['Kundentakt']))
                except ValueError:
                    print(f"Warning: Non-integer value encountered for Order {order_id} in {station}")
                break
        else:
            durations.append(0)
            kundentakts.append(0)

    # Identifying stations with the largest difference and those exceeding Kundentakt
    differences = [d - k for d, k in zip(durations, kundentakts)]
    max_diff_index = differences.index(max(differences, key=abs)) if differences else -1
    exceed_kundentakt_indices = [i for i, diff in enumerate(differences) if diff > 0]

    # Plotting the bars with color coding
    for idx, (station, duration) in enumerate(zip(stations, durations)):
        if idx == max_diff_index:
            color = 'navy'  # Color for the bar with the largest difference
        elif idx in exceed_kundentakt_indices:
            color = 'green'  # Color for bars exceeding Kundentakt
        else:
            color = 'lightblue'  # Default color

        ax.bar(station, duration, color=color, label='Dauerzeit' if idx == 0 else '_nolegend_')
    
    # Setting y-axis limit and labels
    ax.set_ylim(0, 120)
    ax.set_yticks(range(0, 121, 20))

    # Adding data labels on each bar
    for bar in ax.patches:
        ax.annotate(f'{bar.get_height()}',
                    xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')

    # Drawing Kundentakt line and label
    kundentakt_value_for_order = next((k for k in kundentakts if k > 0), 0)
    
    if kundentakt_value_for_order > 0:
        ax.axhline(y=kundentakt_value_for_order, color='red', linestyle='-', linewidth=2, label='Kundentakt')
        ax.text(0.5, kundentakt_value_for_order, f'{kundentakt_value_for_order}', color='red', va='bottom', ha='center')
    
    # Setting chart title and labels
    ax.set_xlabel('Arbeitsstation')
    ax.set_ylabel('Dauerzeit (Sekunden)')
    ax.set_title(f'Dauerzeit vs. Kundentakt für Order {order_id}')
    ax.legend()

    return fig
# Streamlit 应用主函数
def main():
    st.title("Dauerzeit vs. Kundentakt Analyse")

    # 加载所有工作站的数据
    stations_data = {}
    all_orders = set()

    base_path = 'pages'
    for i in range(1, 7):
        filename = os.path.join(base_path, f'Arbeitsstation{i}_durations.json')
        station_data = load_json_data(filename)
        print(f"Arbeitsstation{i} Data:", station_data)  # 打印每个工作站的数据
        stations_data[f'Arbeitsstation{i}'] = station_data
        for record in station_data:
            all_orders.add(record['Order'])
        print("All Orders:", all_orders)  # 打印所有订单，检查是否为空

    # 使用 Streamlit 的 selectbox 让用户选择一个订单
    selected_order = st.selectbox('Bitte wählen sie ein Order aus:', sorted(all_orders))

    # 检查是否选择了订单
    if selected_order:
        # 创建图表
        fig = create_chart(selected_order, stations_data)
        # 使用 Streamlit 的 st.pyplot() 显示图表
        st.pyplot(fig)

if __name__ == "__main__":
    main()
