import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Calculadora de Liquidación de Arroz", page_icon="🌾", layout="centered")

# Estilo CSS para ocultar los elementos de Streamlit al imprimir y mostrar solo el recibo en una página
st.markdown("""
    <style>
    @media print {
        /* Ocultar la barra lateral, botones superiores y menús de Streamlit */
        header, [data-testid="stSidebar"], .stButton, .stNumberInput, footer, hr {
            display: none !important;
        }
        /* Asegurar que el contenedor principal ocupe toda la hoja limpia */
        body, html, [data-testid="stAppViewContainer"] {
            background-color: white !important;
            color: black !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        /* Forzar salto de página limpio */
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
TARA_FIJA = 0.5  # Puedes cambiar este valor aquí si la tara constante es otra

# Entradas del usuario en la interfaz
total_sacos = st.number_input("Total de sacos", min_value=1, value=100, step=1)
peso_bruto = st.number_input("Peso bruto (kg)", min_value=0.0, value=11500.0, step=10.0)

# Mostramos la tara como un valor fijo informativo
st.text(f"Tara por saco (Constante): {TARA_FIJA} kg")

divisor_porcentaje = st.number_input("Divisor por porcentaje (ej. 132 para 32%)", min_value=1.0, value=132.0, step=1.0)
precio_fanega = st.number_input("Precio por fanega (RD$)", min_value=0.0, value=3600.0, step=50.0)

st.markdown("")

# Usamos st.session_state para guardar los resultados y que no se pierdan al interactuar
if "calculado" not in st.session_state:
    st.session_state.calculado = False

# Botón de calcular
if st.button("Calcular Liquidación", type="primary"):
    # 1. Cálculo de tara usando la constante fija y el peso neto
    descuento_tara = total_sacos * TARA_FIJA
    peso_neto = peso_bruto - descuento_tara
    
    # 2. Cálculo de fanegas dividiendo el peso neto entre el divisor ingresado (ej. 132)
    rendimiento_fanegas = peso_neto / divisor_porcentaje
    
    # 3. Total a pagar
    total_a_pagar = rendimiento_fanegas * precio_fanega
    
    # 4. Precio por saco equivalente
    precio_por_saco = total_a_pagar / total_sacos

    # Guardamos todo en la sesión para que no desaparezca
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

# Si ya se calculó, mostramos los resultados fijos en la pantalla
if st.session_state.calculado:
    st.markdown("---")
    
    # Envolvemos el resultado en un div con clase para la impresión limpia
    st.markdown('<div class="recibo-impresion">', unsafe_allow_html=True)
    st.subheader("📊 Resultado de la Liquidación (Recibo)")
    
    st.metric(label="Total a Pagar",
