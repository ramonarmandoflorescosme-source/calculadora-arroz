import os
from PIL import Image
import streamlit as st
from pillow_heif import register_heif_opener

# Registrar soporte para imágenes HEIC (formato de celular)
register_heif_opener()

# Configuración de la página
st.set_page_config(
    page_title="Calculadora de Liquidación de Arroz", page_icon="🌾", layout="centered"
)

st.title("🌾 Calculadora de Liquidación de Arroz")
st.write(
    "Sistema inteligente de liquidación y escaneo de recibos para el sector arrocero."
)

# Barra lateral para configuración
st.sidebar.markdown("### ⚙️ Configuración de Escaneo")
api_key_input = st.sidebar.text_input(
    "Tu API Key de Gemini:", type="password"
)

# Definir la API Key (prioriza la barra lateral, luego secrets si los hubiera)
gemini_key = api_key_input or st.secrets.get("GEMINI_API_KEY", "")

# Sección principal: Carga de recibo o cuaderno
st.markdown("### 📸 Escaneo de Recibo / Cuaderno")
uploaded_file = st.file_uploader(
    "Sube una foto de la factura oficial (JPG, PNG o HEIC):",
    type=["jpg", "jpeg", "png", "heic"],
)

if uploaded_file is not None:
  try:
    image = Image.open(uploaded_file)
    with st.expander("👁️ Ver foto cargada"):
      st.image(image, caption="Recibo cargado", use_container_width=True)

    if not gemini_key:
      st.warning(
          "⚠️ Falta la API Key: Ingrésala en la barra lateral izquierda (⚙️"
          " Configuración de Escaneo) para que la IA lea la foto"
          " automáticamente."
      )
    else:
      # Lógica de procesamiento con Gemini con el modelo actualizado
      import google.generativeai as genai

      genai.configure(api_key=gemini_key)

      with st.spinner("Leyendo recibo con inteligencia artificial..."):
        # Usando el modelo correcto gemini-3.8-flash
        model = genai.GenerativeModel("gemini-3.8-flash")
        prompt = (
            "Extrae los datos clave de este recibo de arroz: nombre del"
            " comprador, peso bruto, descuentos y peso neto en formato"
            " estructurado."
        )
        response = model.generate_content([prompt, image])

        st.success("¡Recibo leído con éxito!")
        st.write(response.text)

  except Exception as e:
    st.error(f"Error procesando la imagen: {e}")

# Formulario de Datos de Liquidación
st.markdown("---")
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
  st.info(
      "Ingresa los datos o usa el escaneo automático superior para ver los"
      " resultados de fanegas y neto a pagar."
  )
