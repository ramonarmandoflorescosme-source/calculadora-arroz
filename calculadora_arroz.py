import streamlit as st

st.set_page_config(page_title="Calculadora de Liquidación de Arroz", page_icon="🌾", layout="centered")

st.title("🌾 Calculadora de Liquidación de Arroz")
st.markdown("---")

# Entradas del usuario en la interfaz
total_sacos = st.number_input("Total de sacos", min_value=1, value=100, step=1)
peso_bruto = st.number_input("Peso bruto (kg)", min_value=0.0, value=11500.0, step=10.0)
tara_por_saco = st.number_input("Tara por saco (kg)", min_value=0.0, value=0.5, step=0.1)
porcentaje_molino = st.number_input("Porcentaje (ej. 32 para 32% / 1.32)", min_value=0.0, value=32.0, step=0.1)
precio_fanega = st.number_input("Precio por fanega (RD$)", min_value=0.0, value=3600.0, step=50.0)

st.markdown("")

# Botón de calcular
if st.button("Calcular Liquidación", type="primary"):
    # 1. Cálculo de tara y peso neto (Peso bruto menos la mitad de la cantidad de sacos o el descuento de tara)
    descuento_tara = total_sacos * tara_por_saco
    peso_neto = peso_bruto - descuento_tara
    
    # 2. Cálculo de fanegas (peso neto dividido entre el porcentaje con el 1 adelante, ej. 1.32)
    divisor = 1.0 + (porcentaje_molino / 100.0)
    rendimiento_fanegas = peso_neto / divisor
    
    # 3. Total a pagar
    total_a_pagar = rendimiento_fanegas * precio_fanega
    
    # 4. Precio por saco equivalente
    precio_por_saco = total_a_pagar / total_sacos
    
    # Mostrar Resultados en pantalla
    st.markdown("---")
    st.subheader("📊 Resultado de la Liquidación")
    
    st.metric(label="Total a Pagar", value=f"RD$ {total_a_pagar:,.2f}")
    
    st.markdown(f"""
    | Concepto | Resultado |
    | :--- | :--- |
    | **Total de sacos** | {total_sacos:,} |
    | **Peso bruto** | {peso_bruto:,.2f} kg |
    | **Tara por saco** | {tara_por_saco:,.2f} kg |
    | **Descuento de tara** | {descuento_tara:,.2f} kg |
    | **Peso neto** | {peso_neto:,.2f} kg |
    | **Porcentaje aplicado** | {porcentaje_molino}% (divisor {divisor}) |
    | **Rendimiento** | {rendimiento_fanegas:,.4f} fanegas |
    | **Precio por fanega** | RD$ {precio_fanega:,.2f} |
    | **Precio por saco** | RD$ {precio_por_saco:,.2f} |
    """)
