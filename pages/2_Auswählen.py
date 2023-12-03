import streamlit as st
import json
import os

# 文件保存路径
file_path = 'C:\Users\zxm14\Documents\GitHub\Montagesimulation\Montagesimulation-Copy\pages\\selections.json'

# 保存选择到文件
def save_selections(selections):
    with open(file_path, 'w') as f:
        json.dump(selections, f)

# 从文件加载选择
def load_selections():
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return {}

# Streamlit 应用
def main():
    st.markdown("# Auswählen ✅")
    st.sidebar.markdown("# Auswählen ✅")

    # 可选的工作流程
    workflows = ["Rädermontage", "Montage Führerhaus", "Auflieger-Fahrgestell", "Montage Auflieger", "Montage Zugmaschine", "Endmontage"]

    # 加载之前的选择
    selections = load_selections()

    # 为每个工作站创建一个选择框，并加载之前的选择
    for i in range(1, 7):
        key = f"Arbeitsstation{i}_workflow"
        default_value = selections.get(key, workflows[0])
        workflow = st.selectbox(f"Arbeitsstation {i}", workflows, index=workflows.index(default_value), key=key)
        selections[key] = workflow

    # 保存按钮
    if st.button("Auswahl speichern"):
        save_selections(selections)
        st.success("Auswahl erfolgreich gespeichert!")

if __name__ == "__main__":
    main()