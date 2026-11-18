import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Calculadora de Liquidación de Arroz", page_icon="🌾", layout="centered"
)

st.title("🌾 Calculadora de Liquidación de Arroz")
st.write(
    "Sistema de liquidación para el sector arrocero (Modo de registro manual)."
)

# Formulario de Datos de Liquidación
st.markdown("### 📋 Datos del recibo")

col1, col2 = st.columns(2)
with col1:
  comprador = st.text_input("Nombre del comprador:")
with col2:
  fecha = st.date_input("Fecha de entrega:")

peso_bruto = st.number_input("Peso Bruto (qq o kg):", min_value=0.0, step=0.1)
humedad = st.slider("Humedad (%):", 10.0, 30.0, 14.0)
impureza = st.slider("Impureza (%):", 0.0, 15.0, 2.0)

st.markdown("---")
if st.button("Calcular Liquidación Final"):
  # Aquí puedes agregar la lógica de cálculo matemático cuando desees
  st.success("¡Datos listos para procesar!")
  st.write(f"**Comprador:** {comprador}")
  st.write(f"**Fecha:** {fecha}")
  st.write(f"**Peso Bruto:** {peso_bruto}")
  st.write(f"**Humedad:** {humedad}%")
  st.write(f"**Impureza:** {impureza}%")
