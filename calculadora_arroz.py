import streamlit as st

st.set_page_config(page_title="Calculadora de Liquidación de Arroz", page_icon="🌾", layout="centered")

st.title("🌾 Calculadora de Liquidación de Arroz")
st.markdown("---")

# Entradas del usuario en la interfaz
total_sacos = st.number_input("Total de sacos", min_value=1, value=100, step=1)
peso_bruto = st.number_input("Peso bruto (kg)", min_value=0.0, value=11500.0, step=10.0)
tara_por_saco = st.number_input("Tara por saco (kg)", min_value=0.0, value=0.5, step=0.1)
divisor_porcentaje = st.number_input("Divisor por porcentaje (ej. 132 para 32%)", min_value=1.0, value=132.0, step=1.0)
precio_fanega = st.number_input("Precio por fanega (RD$)", min_value=0.0, value=3600.0, step=50.0)

st.markdown("")

# Usamos st.session_state para guardar los resultados y que no se borren al interactuar
if "calculado" not in st.session_state:
    st.session_state.calculado = False

# Botón de calcular
if st.button("Calcular Liquidación", type="primary"):
    # 1. Cálculo de tara y peso neto
    descuento_tara = total_sacos * tara_por_saco
    peso_neto = peso_bruto - descuento_tara
    
    # 2. Cálculo de fanegas dividiendo el peso neto entre el divisor ingresado (ej. 132)
    rendimiento_fanegas = peso_neto / divisor_porcentaje
    
    # 3. Total a pagar
    total_a_pagar = rendimiento_fanegas * precio_fanega
    
    # 4. Precio por saco equivalente
    precio_por_saco = total_a_pagar / total_sacos

    # Guardamos todo en la sesión
    st.session_state.calculado = True
    st.session_state.total_sacos = total_sacos
    st.session_state.peso_bruto = peso_bruto
    st.session_state.tara_por_saco = tara_por_saco
    st.session_state.descuento_tara = descuento_tara
    st.session_state.peso_neto = peso_neto
    st.session_state.divisor_porcentaje = divisor_porcentaje
    st.session_state.rendimiento_fanegas = rendimiento_fanegas
    st.session_state.precio_fanega = precio_fanega
    st.session_state.precio_por_saco = precio_por_saco
    st.session_state.total_a_pagar = total_a_pagar

# Si ya se calculó una vez, mantenemos los resultados fijos en la pantalla
if st.session_state.calculado:
    st.markdown("---")
    st.subheader("📊 Resultado de la Liquidación")
    
    st.metric(label="Total a Pagar", value=f"RD$ {st.session_state.total_a_pagar:,.2f}")
    
    # Tabla de resultados
    texto_resultado = f"""
| Concepto | Resultado |
| :--- | :--- |
| **Total de sacos** | {st.session_state.total_sacos:,} |
| **Peso bruto** | {st.session_state.peso_bruto:,.2f} kg |
| **Tara por saco** | {st.session_state.tara_por_saco:,.2f} kg |
| **Descuento de tara** | {st.session_state.descuento_tara:,.2f} kg |
| **Peso neto** | {st.session_state.peso_neto:,.2f} kg |
| **Divisor aplicado** | {st.session_state.divisor_porcentaje} |
| **Rendimiento** | {st.session_state.rendimiento_fanegas:,.4f} fanegas |
| **Precio por fanega** | RD$ {st.session_state.precio_fanega:,.2f} |
| **Precio por saco** | RD$ {st.session_state.precio_por_saco:,.2f} |
| **TOTAL A PAGAR** | **RD$ {st.session_state.total_a_pagar:,.2f}** |
"""
    st.markdown(texto_resultado)

    # Botón o función para descargar en texto/CSV o facilitar la impresión
    st.markdown("### 🖨️ Accpciones")
    
    # Creamos un archivo descargable de texto con el resumen para que nunca se pierda
    archivo_txt = texto_resultado.replace("|", "").replace("**", "")
    st.download_button(
        label="📥 Descargar Liquidación en Texto",
        data=archivo_txt,
        file_name="liquidacion_arroz.txt",
        mime="text/plain"
    )
    
    st.info("💡 Consejo para imprimir: Puedes presionar las teclas **Ctrl + P** en tu navegador para imprimir esta página directamente como factura o recibo.")
