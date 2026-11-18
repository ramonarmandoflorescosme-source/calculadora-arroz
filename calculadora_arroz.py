import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Calculadora de Liquidación de Arroz", page_icon="🌾", layout="centered")

# Estilo CSS para ocultar los elementos de Streamlit al imprimir y mostrar solo el recibo en una página
st.markdown("""
    <style>
    @media print {
        header, [data-testid="stSidebar"], .stButton, .stNumberInput, footer, hr {
            display: none !important;
        }
        body, html, [data-testid="stAppViewContainer"] {
            background-color: white !important;
            color: black !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        .recibo-impresion {
            page-break-inside: avoid;
            margin: 0 auto;
            width: 100%;
        }
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌾 Calculadora de Liquidación de Arroz")
st.markdown("---")

# Constante fija para la tara por saco
TARA_FIJA = 0.5  

# Entradas del usuario en la interfaz
total_sacos = st.number_input("Total de sacos", min_value=1, value=100, step=1)
peso_bruto = st.number_input("Peso bruto (kg)", min_value=0.0, value=11500.0, step=10.0)

st.text(f"Tara por saco (Constante): {TARA_FIJA} kg")

divisor_porcentaje = st.number_input("Divisor por porcentaje (ej. 132 para 32%)", min_value=1.0, value=132.0, step=1.0)
precio_fanega = st.number_input("Precio por fanega (RD$)", min_value=0.0, value=3600.0, step=50.0)

st.markdown("")

if "calculado" not in st.session_state:
    st.session_state.calculado = False

# Botón de calcular
if st.button("Calcular Liquidación", type="primary"):
    descuento_tara = total_sacos * TARA_FIJA
    peso_neto = peso_bruto - descuento_tara
    
    rendimiento_fanegas = peso_neto / divisor_porcentaje
    total_a_pagar = rendimiento_fanegas * precio_fanega
    precio_por_saco = total_a_pagar / total_sacos

    st.session_state.calculado = True
    st.session_state.total_sacos = total_sacos
    st.session_state.peso_bruto = peso_bruto
    st.session_state.tara_por_saco = TARA_FIJA
    st.session_state.descuento_tara = descuento_tara
    st.session_state.peso_neto = peso_neto
    st.session_state.divisor_porcentaje = divisor_porcentaje
    st.session_state.rendimiento_fanegas = rendimiento_fanegas
    st.session_state.precio_fanega = precio_fanega
    st.session_state.precio_por_saco = precio_por_saco
    st.session_state.total_a_pagar = total_a_pagar

if st.session_state.calculado:
    st.markdown("---")
    
    st.markdown('<div class="recibo-impresion">', unsafe_allow_html=True)
    st.subheader("📊 Resultado de la Liquidación (Recibo)")
    
    st.metric(label="Total a Pagar", value=f"RD$ {st.session_state.total_a_pagar:,.2f}")
    
    texto_resultado = f"""
| Concepto | Resultado |
| :--- | :--- |
| **Total de sacos** | {st.session_state.total_sacos:,} |
| **Peso bruto** | {st.session_state.peso_bruto:,.2f} kg |
| **Tara por saco (Constante)** | {st.session_state.tara_por_saco:,.2f} kg |
| **Descuento de tara** | {st.session_state.descuento_tara:,.2f} kg |
| **Peso neto** | {st.session_state.peso_neto:,.2f} kg |
| **Divisor aplicado** | {st.session_state.divisor_porcentaje} |
| **Rendimiento** | {st.session_state.rendimiento_fanegas:,.4f} fanegas |
| **Precio por fanega** | RD$ {st.session_state.precio_fanega:,.2f} |
| **Precio por saco** | RD$ {st.session_state.precio_por_saco:,.2f} |
| **TOTAL A PAGAR** | **RD$ {st.session_state.total_a_pagar:,.2f}** |
"""
    st.markdown(texto_resultado)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 🖨️ Opciones y Descarga")
    
    archivo_txt = texto_resultado.replace("|", "").replace("**", "")
    st.download_button(
        label="📥 Descargar Liquidación en Texto",
        data=archivo_txt,
        file_name="liquidacion_arroz.txt",
        mime="text/plain"
    )
    
    boton_imprimir_html = """
    <script>
    function triggerPrint() {
        window.parent.print();
    }
    </script>
    <button onclick="triggerPrint()" style="
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 0.5rem;
        font-weight: 600;
        cursor: pointer;
        font-size: 16px;
        margin-top: 10px;
    ">
        🖨️ Imprimir Recibo en una Sola Página
    </button>
    """
    components.html(boton_imprimir_html, height=60)
