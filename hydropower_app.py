import streamlit as st
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# 页面配置
st.set_page_config(page_title="Hydropower Design App", layout="wide")

# 顶部图片
image = Image.open("Snowy_2.0_1.webp")
st.image(image, use_container_width=True)

# 功能选择菜单
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

# Power Calculation 页面：保留原有功能
if menu == "Power Calculation":
    st.title("🔋 Power Calculation")
    st.markdown("Compute power and energy output based on hydraulic design parameters.")

    def estimate_d_h(Q):
        a = 1.2
        b = 1.5
        return a * np.log(Q) + b

    def calculate_gross_head(HWL, LWL, TWL):
        NWL = (2/3) * HWL + (1/3) * LWL
        return NWL - TWL

    def calculate_h_draft(h_gross):
        return -1.87e-5 * h_gross**2 - 0.0172 * h_gross + 51.70

    def calculate_reynolds(u, d_h, nu=1e-6):
        return u * d_h / nu

    def calculate_lambda(re, k, d_h, max_iter=100):
        if re < 2300:
            return 64 / re
        lambda_guess = 0.02
        for _ in range(max_iter):
            right = -2 * np.log10((2.51 / (re * np.sqrt(lambda_guess))) + (k / d_h) / 3.72)
            lambda_guess = (1 / right) ** 2
        return lambda_guess

    def delta_h_major_loss(lmbda, l, d_h, u, rho_f=1000, rho_w=1000, g=9.81):
        return lmbda * (l / d_h) * (u ** 2 / (2 * g)) * (rho_f / rho_w)

    def calculate_effective_head(h_gross, h_major_loss, h_draft):
        return h_gross - h_major_loss - h_draft

    def calculate_power(Q, h, g, eta):
        return Q * h * g * eta

    def calculate_energy(P, T):
        return P * T

    # 用户输入
    st.sidebar.header("📥 Input Parameters")
    Q = st.sidebar.number_input("Design discharge Q (m³/s)", value=56.25)
    HWL = st.sidebar.number_input("High Water Level (HWL) (m)", value=400.0)
    LWL = st.sidebar.number_input("Low Water Level (LWL) (m)", value=370.0)
    TWL = st.sidebar.number_input("Tailwater Level (TWL) (m)", value=300.0)
    l = st.sidebar.number_input("Pipe Length l (m)", value=500.0)
    k = st.sidebar.number_input("Pipe Roughness k (m)", value=0.0006)
    u = st.sidebar.number_input("Flow Velocity u (m/s)", value=5.0)
    nu = st.sidebar.number_input("Kinematic Viscosity ν (m²/s)", value=1e-6)
    eta = st.sidebar.slider("Efficiency η", 0.0, 1.0, 0.85)
    T = st.sidebar.number_input("Operating Time T (h)", value=24.0)

    d_h = estimate_d_h(Q)
    st.sidebar.markdown(f"### Estimated d_h: **{d_h:.2f} m**")

    h_gross = calculate_gross_head(HWL, LWL, TWL)
    h_draft = calculate_h_draft(h_gross)
    re = calculate_reynolds(u, d_h, nu)
    lmbda = calculate_lambda(re, k, d_h)
    h_major_loss = delta_h_major_loss(lmbda, l, d_h, u)
    h_effective = calculate_effective_head(h_gross, h_major_loss, h_draft)
    P = calculate_power(Q, h_effective, 9.81, eta)
    E = calculate_energy(P, T)

    st.header("📊 Output Results")
    st.metric("Gross Head (m)", f"{h_gross:.2f}")
    st.metric("Draft Head (m)", f"{h_draft:.2f}")
    st.metric("Head Loss (m)", f"{h_major_loss:.2f}")
    st.metric("Effective Head (m)", f"{h_effective:.2f}")
    st.metric("Power Output (kW)", f"{P:.2f}")
    st.metric("Energy Output (kWh)", f"{E:.2f}")

    with st.expander("🔍 Technical Details"):
        st.write(f"Reynolds Number: {re:,.0f}")
        st.write(f"Friction Coefficient (λ): {lmbda:.5f}")

    # 图表展示：Q vs d_h
    Q_values = np.linspace(10, 150, 100)
    d_h_values = estimate_d_h(Q_values)
    fig1, ax1 = plt.subplots()
    ax1.plot(Q_values, d_h_values)
    ax1.set_xlabel("Design Discharge Q (m³/s)")
    ax1.set_ylabel("Hydraulic Diameter d_h (m)")
    ax1.set_title("Q vs. d_h")
    st.pyplot(fig1)

    # 图表展示：能量变化图
    T_hours = np.linspace(0, 48, 100)
    E_values = P * T_hours
    fig2, ax2 = plt.subplots()
    ax2.plot(T_hours, E_values)
    ax2.set_xlabel("Operating Time (h)")
    ax2.set_ylabel("Energy Output (kWh)")
    ax2.set_title("Energy Output over Time")
    st.pyplot(fig2)

# 其他功能暂留空
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
