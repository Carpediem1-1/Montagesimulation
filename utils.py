# utils.py
import streamlit as st

def display_order_info(item):
    """显示订单信息，特定字段以绿色高亮显示，常规内容以灰色显示"""

    # 常规信息，冒号后的信息以灰色显示
    st.markdown(f"<h4>Bestelldatum und Uhrzeit: <span style='color: grey;'>{item.get('Bestelldatum und Uhrzeit', 'N/A')}</span></h4>", unsafe_allow_html=True)
    st.markdown(f"<h4>Kunde: <span style='color: grey;'>{item.get('Kunde', 'N/A')}</span></h4>", unsafe_allow_html=True)
    st.markdown(f"<h4>Auftragsnummer: <span style='color: grey;'>{item.get('Auftragsnummer', 'N/A')}</span></h4>", unsafe_allow_html=True)
    st.markdown(f"<h4>Kundentakt: <span style='color: grey;'>{item.get('Kundentakt', 'N/A')}</span></h4>", unsafe_allow_html=True)

    # 高亮显示的字段，只有当它们存在于 JSON 数据中时
    highlight_keys = ['Sonderwunsch', 'Achse', 'Reifen', 'Sidepipes','Führerhaus']
    for key in highlight_keys:
        if key in item:
            st.markdown(f"<h4>{key}: <span style='color: green;'>{item[key]}</span></h4>", unsafe_allow_html=True)

    # 如果存在，则显示 Container 信息
    for i in range(1, 5):
        container_key = f"Container {i}"
        if container_key in item:
            st.markdown(f"<h4>{container_key}: <span style='color: green;'>{item[container_key]}</span></h4>", unsafe_allow_html=True)