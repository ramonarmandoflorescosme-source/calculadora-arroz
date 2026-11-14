
import streamlit as st
import streamlit.components.v1 as components
from datetime import date
from html import escape

st.set_page_config(
    page_title="Liquidación de Arroz",
    page_icon="🌾",
    layout="centered"
)

st.title("🌾 LIQUIDADORA DE ARROZ")
st.write("Sistema de cálculo y control de liquidaciones de arroz.")

st.markdown("---")

# ==================================
# 1. DATOS DEL COMPRADOR Y RECIBO
# ==================================

st.header("📋 Datos del recibo")

comprador = st.text_input("Nombre del comprador:")
productor = st.text_input("Nombre del productor:")
molino = st.text_input("Nombre del molino:")
numero_recibo = st.text_input("Número de recibo:")
fecha_recibo = st.date_input("Fecha del recibo", value=date.today())

variedad = st.text_input("Variedad de arroz:")

st.markdown("---")

# ==================================
# 2. METODO DE ENTRADA
# ==================================

st.header("⚖️ Datos del peso")

modo = st.radio(
    "Selecciona el método de entrada:",
    ["Peso Bruto Total (kg)", "Por Pesadas (Báscula)"]
)

if modo == "Peso Bruto Total (kg)":

    total_sacos = st.number_input(
        "Total de sacos:",
        min_value=0,
        value=0,
        step=1
    )

    peso_bruto = st.number_input(
        "Peso bruto total (kg):",
        min_value=0.0,
        value=0.0,
        step=10.0
    )

else:

    num_pesadas = st.number_input(
        "Número de pesadas:",
        min_value=0,
        value=0,
        step=1
    )

    sacos_pesada = st.number_input(
        "Sacos por cada pesada:",
        min_value=0,
        value=0,
        step=1
    )

    kilos_pesada = st.number_input(
        "Kilos por pesada (kg):",
        min_value=0.0,
        value=0.0,
        step=10.0
    )

    total_sacos = num_pesadas * sacos_pesada
    peso_bruto = num_pesadas * kilos_pesada

# ==================================
# 3. DATOS DE LIQUIDACION
# ==================================

st.markdown("---")
st.header("💰 Datos de liquidación")

tara_por_saco = st.number_input(
    "Tara por saco (kg):",
    min_value=0.0,
    value=0.5,
    step=0.1
)

porcentaje_molino = st.number_input(
    "Porcentaje del molino (%):",
    min_value=0.0,
    max_value=100.0,
    value=40.0,
    step=1.0
)

precio_fanega = st.number_input(
    "Precio por fanega (RD$):",
    min_value=0.0,
    value=3600.0,
    step=100.0
)

observaciones = st.text_area("Observaciones:")

# ==================================
# 4. CALCULAR LIQUIDACION
# ==================================

st.markdown("---")

if st.button("CALCULAR LIQUIDACIÓN", type="primary"):

    if total_sacos <= 0 or peso_bruto <= 0:

        st.warning("Ingresa una cantidad válida de sacos y peso bruto.")

    elif peso_bruto - (total_sacos * tara_por_saco) <= 0:

        st.warning("El peso neto debe ser mayor que cero.")

    else:

        tara_sacos = total_sacos * tara_por_saco

        peso_neto = peso_bruto - tara_sacos

        rendimiento_fanegas = (
            peso_neto * (porcentaje_molino / 100)
        ) / 56.0

        total_pagar = rendimiento_fanegas * precio_fanega

        precio_por_saco = total_pagar / total_sacos

        # Guardar resultados en la sesión
        st.session_state["liquidacion"] = {
            "comprador": comprador,
            "productor": productor,
            "molino": molino,
            "numero_recibo": numero_recibo,
            "fecha": fecha_recibo.strftime("%d/%m/%Y"),
            "variedad": variedad,
            "modo": modo,
            "total_sacos": total_sacos,
            "peso_bruto": peso_bruto,
            "tara_por_saco": tara_por_saco,
            "tara_sacos": tara_sacos,
            "peso_neto": peso_neto,
            "porcentaje_molino": porcentaje_molino,
            "rendimiento": rendimiento_fanegas,
            "precio_fanega": precio_fanega,
            "total_pagar": total_pagar,
            "precio_por_saco": precio_por_saco,
            "observaciones": observaciones
        }

# ==================================
# 5. MOSTRAR RESULTADOS
# ==================================

if "liquidacion" in st.session_state:

    datos = st.session_state["liquidacion"]

    st.markdown("---")
    st.header("📊 RESULTADOS DE LA LIQUIDACIÓN")

    st.metric("Peso neto real", f"{datos['peso_neto']:,.2f} kg")

    st.metric(
        "Rendimiento",
        f"{datos['rendimiento']:,.4f} fanegas"
    )

    st.metric(
        "Total a pagar",
        f"RD$ {datos['total_pagar']:,.2f}"
    )

    st.metric(
        "Precio por saco",
        f"RD$ {datos['precio_por_saco']:,.2f}"
    )

    # ==================================
    # 6. COMPROBANTE PARA IMPRIMIR
    # ==================================

    st.markdown("---")
    st.header("🖨️ Comprobante de liquidación")

    d = datos

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
            color: #222;
        }}

        .recibo {{
            max-width: 700px;
            margin: auto;
            border: 1px solid #999;
            padding: 25px;
        }}

        h1, h2 {{
            text-align: center;
        }}

        .subtitulo {{
            text-align: center;
            font-size: 13px;
        }}

        .datos {{
            line-height: 1.9;
            margin-top: 20px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}

        th, td {{
            border: 1px solid #999;
            padding: 9px;
            text-align: left;
        }}

        th {{
            background: #eeeeee;
        }}

        .total {{
            margin-top: 20px;
            padding: 15px;
            background: #eeeeee;
            font-size: 22px;
            font-weight: bold;
            text-align: right;
        }}

        .firmas {{
            display: flex;
            justify-content: space-between;
            margin-top: 65px;
            gap: 30px;
        }}

        .firma {{
            width: 50%;
            text-align: center;
            border-top: 1px solid #333;
            padding-top: 8px;
        }}

        .observaciones {{
            margin-top: 25px;
            min-height: 45px;
        }}

        @media print {{
            .no-imprimir {{
                display: none;
            }}

            body {{
                padding: 0;
            }}

            .recibo {{
                border: none;
            }}
        }}
    </style>
    </head>

    <body>

    <div class="recibo">

        <h1>🌾 LIQUIDADORA DE ARROZ</h1>
        <h2>COMPROBANTE DE CÁLCULO</h2>

        <p class="subtitulo">
            CONTROL DEL COMPRADOR
        </p>

        <hr>

        <div class="datos">

            <b>COMPRADOR:</b> {escape(d['comprador'])}<br>

            <b>PRODUCTOR:</b> {escape(d['productor'])}<br>

            <b>MOLINO:</b> {escape(d['molino'])}<br>

            <b>NÚMERO DE RECIBO:</b> {escape(d['numero_recibo'])}<br>

            <b>FECHA:</b> {escape(d['fecha'])}<br>

            <b>VARIEDAD DE ARROZ:</b> {escape(d['variedad'])}

        </div>

        <hr>

        <h3>DETALLE DE LA LIQUIDACIÓN</h3>

        <table>

            <tr>
                <th>Concepto</th>
                <th>Resultado</th>
            </tr>

            <tr>
                <td>Total de sacos</td>
                <td>{d['total_sacos']}</td>
            </tr>

            <tr>
                <td>Peso bruto</td>
                <td>{d['peso_bruto']:,.2f} kg</td>
            </tr>

            <tr>
                <td>Tara por saco</td>
                <td>{d['tara_por_saco']:.2f} kg</td>
            </tr>

            <tr>
                <td>Descuento de tara</td>
                <td>{d['tara_sacos']:,.2f} kg</td>
            </tr>

            <tr>
                <td>Peso neto</td>
                <td>{d['peso_neto']:,.2f} kg</td>
            </tr>

            <tr>
                <td>Porcentaje del molino</td>
                <td>{d['porcentaje_molino']:.2f}%</td>
            </tr>

            <tr>
                <td>Rendimiento</td>
                <td>{d['rendimiento']:,.4f} fanegas</td>
            </tr>

            <tr>
                <td>Precio por fanega</td>
                <td>RD$ {d['precio_fanega']:,.2f}</td>
            </tr>

            <tr>
                <td>Precio por saco</td>
                <td>RD$ {d['precio_por_saco']:,.2f}</td>
            </tr>

        </table>

        <div class="total">
            TOTAL A PAGAR:
            RD$ {d['total_pagar']:,.2f}
        </div>

        <div class="observaciones">
            <b>OBSERVACIONES:</b><br>
            {escape(d['observaciones']).replace(chr(10), '<br>')}
        </div>

        <div class="firmas">

            <div class="firma">
                Firma del comprador
            </div>

            <div class="firma">
                Firma de recibido
            </div>

        </div>

        <hr>

        <p class="subtitulo">
            Documento de control interno.
            No sustituye el recibo original.
        </p>

    </div>

    <div class="no-imprimir" style="text-align:center; margin-top:20px;">
        <button onclick="window.print()"
        style="padding:12px 25px; font-size:16px;
        background:#168342; color:white;
        border:0; border-radius:6px;">
            🖨️ IMPRIMIR COMPROBANTE
        </button>
    </div>

    </body>
    </html>
    """

    components.html(html, height=1100, scrolling=True)
