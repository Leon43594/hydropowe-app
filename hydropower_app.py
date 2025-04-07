import streamlit as st
import numpy as np
from PIL import Image

# 页面配置
st.set_page_config(page_title="Hydropower Design App", layout="wide")

# 顶部横幅图片
image = Image.open("Snowy_2.0_1.webp")
st.image(image, use_container_width=True)

# 顶部导航菜单
menu = st.sidebar.radio(
    "Select a Function",
    (
        "Power Calculation",
        "Discharge Simulation",
        "Civil Work Design",
        "Turbine",
        "Power Station Plan",
        "Site Selection"
    )
)

# 主功能模块页面
if menu == "Power Calculation":
    st.title("🔋 Power Calculation")
    st.markdown("This section will calculate power and energy output based on hydraulic head and flow rate.")

elif menu == "Discharge Simulation":
    st.title("🌊 Discharge Simulation")
    st.markdown("This section will simulate water discharge over time or under different conditions.")

elif menu == "Civil Work Design":
    st.title("🏗️ Civil Work Design")
    st.markdown("This section will provide tools for designing tunnels, penstocks, and structural components.")

elif menu == "Turbine":
    st.title("⚙️ Turbine")
    st.markdown("This section will include turbine selection, sizing, and efficiency calculations.")

elif menu == "Power Station Plan":
    st.title("🏭 Power Station Plan")
    st.markdown("This section will provide layout planning tools for a hydropower station.")

elif menu == "Site Selection":
    st.title("📍 Site Selection")
    st.markdown("This section will include tools for evaluating and selecting optimal hydropower sites using data.")
