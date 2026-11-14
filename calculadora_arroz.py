import streamlit as st

st.set_page_config(page_title="Liquidación de Arroz", page_icon="🌾", layout="centered")

st.title("🌾 Liquidación de Arroz")
st.write("Calcula el rendimiento, peso neto y total a pagar de tu cosecha.")

modo = st.radio("Selecciona el método de entrada:", ["Peso Bruto Total (kg)", "Por Pesadas (Báscula)"])

st.markdown("---")

if modo == "Peso Bruto Total (kg)":
    total_sacos = st.number_input("Total de Sacos en el recibo:", min_value=0, value=None, step=1, placeholder="Ej. 92")
    peso_bruto = st.number_input("Peso Bruto Total (kg) [Suma de la báscula]:", min_value=0.0, value=None, step=10.0, placeholder="Ej. 10120")
    
    sacos_val = total_sacos if total_sacos is not None else 0
    bruto_val = peso_bruto if peso_bruto is not None else 0.0
    
    tara_sacos = sacos_val * 0.5
    peso_neto = bruto_val - tara_sacos
else:
    num_pesadas = st.number_input("Número de pesadas:", min_value=0, value=None, step=1, placeholder="Ej. 30")
    sacos_pesada = st.number_input("Sacos por cada pesada:", min_value=0, value=None, step=1, placeholder="Ej. 3")
    kilos_pesada = st.number_input("Kilos por pesada (kg):", min_value=0.0, value=None, step=10.0, placeholder="Ej. 300")
    
    p_num = num_pesadas if num_pesadas is not None else 0
    p_sac = sacos_pesada if sacos_pesada is not None else 0
    p_kil = kilos_pesada if kilos_pesada is not None else 0.0
    
    total_sacos = p_num * p_sac
    peso_bruto = p_num * p_kil
    tara_sacos = total_sacos * 0.5
    peso_neto = peso_bruto - tara_sacos

porcentaje_molino = st.number_input("Porcentaje del molino (ej. 33 o 40):", min_value=0.0, max_value=100.0, value=40.0, step=1.0)
precio_fanega = st.number_input("Precio por Fanega ($):", min_value=0.0, value=3600.0, step=100.0)

st.markdown("")

if st.button("CALCULAR LIQUIDACIÓN", type="primary"):
    sacos_final = total_sacos if total_sacos is not None else 0
    bruto_final = peso_bruto if peso_bruto is not None else 0.0
    
    if sacos_final > 0 and bruto_final > 0:
        rendimiento_fanegas = (peso_neto * (porcentaje_molino / 100)) / 56.0
        total_pagar = rendimiento_fanegas * precio_fanega
        precio_por_saco = total_pagar / sacos_final if sacos_final > 0 else 0

        st.markdown("### 📊 RESULTADOS DE LA LIQUIDACIÓN:")
        st.success(f"""
        - **Total de Sacos:** {int(sacos_final)}
        - **Peso Bruto Total:** {bruto_final:,.2f} kg
        - **Descuento (Sacos):** {tara_sacos:,.2f} kg
        - **Peso Neto Real:** {peso_neto:,.2f} kg
        - **Rendimiento (Fanegas):** {rendimiento_fanegas:,.4f}
        - **Total a Pagar:** ${total_pagar:,.2f}
        - **Precio por Saco:** ${precio_por_saco:,.2f}
        """)
    else:
        st.warning("⚠️ Por favor ingresa los datos de sacos y peso bruto para poder calcular.")
