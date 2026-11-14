import streamlit as st

st.set_page_config(page_title="Calculadora de Arroz", page_icon="🌾", layout="centered")

st.title("🌾 Calculadora Agrícola - Producción de Arroz")
st.markdown("Herramienta para estimar costos, rendimiento por tarea y rentabilidad.")

# --- DATOS EN LA PÁGINA PRINCIPAL ---
st.subheader("📝 Datos de la Parcela")
col_var, col_tar = st.columns(2)
with col_var:
    variedad = st.text_input("Variedad de Arroz", value="Juma 69-20 (Jaragua)")
with col_tar:
    tareas = st.number_input("Área sembrada (Tareas)", min_value=1.0, value=22.0, step=1.0)

# Barra lateral para costos y rendimiento
st.sidebar.header("Costos de Insumos y Mano de Obra")
costo_preparacion = st.sidebar.number_input("Preparación de tierra y siembra ($)", min_value=0.0, value=15000.0, step=500.0)
costo_fertilizantes = st.sidebar.number_input("Costo de Fertilización (Urea, 15-15-15, foliares) ($)", min_value=0.0, value=12000.0, step=500.0)
costo_quimicos = st.sidebar.number_input("Control de plagas/enfermedades (Fungicidas/Herbicidas) ($)", min_value=0.0, value=8000.0, step=500.0)
costo_riego_labores = st.sidebar.number_input("Agua, riego y otras labores ($)", min_value=0.0, value=6000.0, step=500.0)

st.sidebar.header("Cosecha y Ventas")
rendimiento_fanegas_por_tarea = st.sidebar.number_input("Rendimiento estimado (Fanegas por tarea)", min_value=0.0, value=2.5, step=0.1)
precio_por_fanega = st.sidebar.number_input("Precio de venta por Fanega ($)", min_value=0.0, value=3200.0, step=100.0)

# Cálculos
total_costos = costo_preparacion + costo_fertilizantes + costo_quimicos + costo_riego_labores
total_fanegas = tareas * rendimiento_fanegas_por_tarea
ingreso_total = total_fanegas * precio_por_fanega
beneficio_neto = ingreso_total - total_costos
costo_por_tarea = total_costos / tareas if tareas > 0 else 0
rentabilidad = (beneficio_neto / total_costos * 100) if total_costos > 0 else 0

# Resultados en pantalla principal
st.markdown("---")
st.subheader("📊 Resumen Financiero y Productivo")

# Recuadro destacado con la variedad y superficie actualizada
st.info(f"🌱 **Variedad:** {variedad if variedad else 'No especificada'}  |  📐 **Superficie:** {tareas} tareas")

col1, col2 = st.columns(2)
with col1:
    st.metric("Inversión / Costo Total", f"${total_costos:,.2f}")
    st.metric("Costo por Tarea", f"${costo_por_tarea:,.2f}")
    st.metric("Producción Total Estimada", f"{total_fanegas:.1f} Fanegas")

with col2:
    st.metric("Ingreso Bruto", f"${ingreso_total:,.2f}")
    st.metric("Beneficio Neto (Ganancia)", f"${beneficio_neto:,.2f}")
    st.metric("Rentabilidad", f"{rentabilidad:.1f}%")
