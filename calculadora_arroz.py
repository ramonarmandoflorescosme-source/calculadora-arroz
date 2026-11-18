from datetime import datetime
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Liquidadora de Arroz - RAFC", page_icon="🌾", layout="centered"
)

# Título y Encabezado igual al diseño original
st.markdown(
    "<h2 style='text-align: center;'>🌾 LIQUIDADORA DE ARROZ</h2>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h4 style='text-align: center;'>COMPROBANTE DE CÁLCULO</h4>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: gray;'>CONTROL DEL COMPRADOR</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Datos del encabezado del recibo
col1, col2 = st.columns(2)
with col1:
  comprador = st.text_input("COMPRADOR:")
  molino = st.text_input("MOLINO:")
  fecha = st.date_input("FECHA:", value=datetime.today())
with col2:
  productor = st.text_input("PRODUCTOR:")
  num_recibo = st.text_input("NÚMERO DE RECIBO:")
  variedad = st.text_input("VARIEDAD DE ARROZ:", value="Juma 69-20")

st.markdown("---")
st.markdown("### DETALLE DE LA LIQUIDACIÓN")

# Entradas para los cálculos
total_sacos = st.number_input(
    "Total de sacos", min_value=0, value=100, step=1
)
peso_bruto = st.number_input(
    "Peso bruto (kg)", min_value=0.0, value=11500.0, step=10.0
)
tara_por_saco = st.number_input(
    "Tara por saco (kg)", min_value=0.0, value=0.50, step=0.05
)
porcentaje_molino = (
    st.slider("Porcentaje del molino (%)", 0.0, 100.0, 40.0, 0.5) / 100.0
)
precio_fanega = st.number_input(
    "Precio por fanega (RD$)", min_value=0.0, value=3600.0, step=50.0
)

# Cálculos automáticos basados en tu estructura
descuento_tara = total_sacos * tara_por_saco
peso_neto = peso_bruto - descuento_tara
# Estimación estándar de rendimiento en fanegas (ejemplo de conversión a fanegas arroceras)
rendimiento_fanegas = (
    peso_neto * porcentaje_molino
) / 50.0  # Ajustable según la fórmula de fanegas local
total_a_pagar = rendimiento_fanegas * precio_fanega
precio_por_saco = total_a_pagar / total_sacos if total_sacos > 0 else 0.0

st.markdown("---")

# Tabla de resultados visual estilo comprobante
st.markdown("### 📊 Resultado de la Liquidación")

st.markdown(f"""
| Concepto | Resultado |
| :--- | :--- |
| **Total de sacos** | {total_sacos} |
| **Peso bruto** | {peso_bruto:,.2f} kg |
| **Tara por saco** | {tara_por_saco:,.2f} kg |
| **Descuento de tara** | {descuento_tara:,.2f} kg |
| **Peso neto** | {peso_neto:,.2f} kg |
| **Porcentaje del molino** | {porcentaje_molino * 100:.2f}% |
| **Rendimiento** | {rendimiento_fanegas:,.4f} fanegas |
| **Precio por fanega** | RD$ {precio_fanega:,.2f} |
| **Precio por saco** | RD$ {precio_por_saco:,.2f} |
""")

# Cuadro destacado del Total a Pagar
st.markdown(
    f"<h3 style='text-align: center; background-color: #f0f2f6; padding:"
    f" 15px; border-radius: 8px;'>TOTAL A PAGAR: RD$ {total_a_pagar:,.2f}</h3>",
    unsafe_allow_html=True,
)

st.markdown("---")
st.markdown("**OBSERVACIONES:**")
observaciones = st.text_area(
    "Notas adicionales", placeholder="Escribe aquí cualquier observación..."
)

st.markdown("<br><br>", unsafe_allow_html=True)
col_f1, col_f2 = st.columns(2)
with col_f1:
  st.markdown(
      "<hr style='border: 1px solid black;'>", unsafe_allow_html=True
  )
  st.markdown(
      "<p style='text-align: center;'>Firma del comprador</p>",
      unsafe_allow_html=True,
  )
with col_f2:
  st.markdown(
      "<hr style='border: 1px solid black;'>", unsafe_allow_html=True
  )
  st.markdown(
      "<p style='text-align: center;'>Firma de recibido</p>",
      unsafe_allow_html=True,
  )

st.markdown(
    "<p style='text-align: center; font-size: small; color: gray;'>Documento"
    " de control interno. No sustituye el recibo original.<br>CREADA POR"
    " RAFC</p>",
    unsafe_allow_html=True,
)
