
import streamlit as st
import streamlit.components.v1 as components
from datetime import date
from html import escape

# ==================================================
# RAFC 2026 - SISTEMA DE LIQUIDACION DE ARROZ
# ==================================================

st.set_page_config(
    page_title="RAFC - Liquidacion de Arroz",
    page_icon="🌾",
    layout="centered"
)

TARA_FIJA = 0.50
AUTOR = "Created by RAFC 2026"

# ==================================================
# ESTILOS GENERALES
# ==================================================

st.markdown("""
<style>
.stApp {
    background-color: #f5f8f4;
}

.titulo-rafc {
    text-align: center;
    color: #17632f;
    font-size: 42px;
    font-weight: bold;
}

.subtitulo-rafc {
    text-align: center;
    color: #45634b;
    font-size: 17px;
}

.tarjeta {
    background: white;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #dce8dc;
    margin-bottom: 12px;
}

.stButton > button {
    border-radius: 10px;
    min-height: 45px;
    font-weight: 600;
}

@media print {
    @page {
        size: A4 portrait;
        margin: 8mm;
    }
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# NAVEGACION
# ==================================================

if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"

if "resultado" not in st.session_state:
    st.session_state.resultado = None


# ==================================================
# FUNCION: PANTALLA PRINCIPAL
# ==================================================

def pantalla_inicio():

    st.markdown("""
    <div style="text-align:center; padding:15px;">
        <div style="font-size:85px;">🌾</div>
        <div class="titulo-rafc">RAFC</div>
        <div class="subtitulo-rafc">
            SISTEMA DE LIQUIDACION DE ARROZ
        </div>
        <hr>
        <h3 style="color:#17632f;">
            Bienvenido a RAFC 2026
        </h3>
        <p>Gestion y control de liquidacion de arroz</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### MENU PRINCIPAL")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🌾 Nueva liquidacion", use_container_width=True):
            st.session_state.pagina = "liquidacion"
            st.rerun()

    with col2:
        if st.button("🧮 Calculadora", use_container_width=True):
            st.session_state.pagina = "calculadora"
            st.rerun()

    st.markdown("---")

    st.markdown("""
    <div style="text-align:center;color:#47704e;">
        <b>RAFC 2026</b><br>
        Sistema de Liquidacion de Arroz
    </div>
    """, unsafe_allow_html=True)


# ==================================================
# FUNCION: CALCULADORA GENERAL
# ==================================================

def calculadora_general():

    st.markdown('<div class="titulo-rafc">🧮 CALCULADORA</div>',
                unsafe_allow_html=True)

    st.markdown("### Operaciones matematicas")

    numero1 = st.number_input(
        "Primer numero",
        value=0.0,
        key="calc_num1"
    )

    numero2 = st.number_input(
        "Segundo numero",
        value=0.0,
        key="calc_num2"
    )

    operacion = st.selectbox(
        "Operacion",
        ["Suma (+)", "Resta (-)", "Multiplicacion (×)",
         "Division (÷)", "Porcentaje (%)"]
    )

    if st.button("Calcular", type="primary"):
        if operacion == "Suma (+)":
            resultado = numero1 + numero2

        elif operacion == "Resta (-)":
            resultado = numero1 - numero2

        elif operacion == "Multiplicacion (×)":
            resultado = numero1 * numero2

        elif operacion == "Division (÷)":
            if numero2 == 0:
                st.error("No se puede dividir entre cero.")
                resultado = None
            else:
                resultado = numero1 / numero2

        else:
            resultado = numero1 * numero2 / 100

        if resultado is not None:
            st.success(f"Resultado: {resultado:,.4f}")

    st.markdown("---")

    if st.button("⬅ Volver al inicio"):
        st.session_state.pagina = "inicio"
        st.rerun()


# ==================================================
# FUNCION: CREAR RECIBO
# ==================================================

def crear_recibo(datos):

    productor = escape(datos["productor"])
    comprador = escape(datos["comprador"])
    variedad = escape(datos["variedad"])

    fecha_texto = datos["fecha"].strftime("%d/%m/%Y")

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">

    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>

    <style>

    @page {{
        size: A4 portrait;
        margin: 8mm;
    }}

    * {{
        box-sizing: border-box;
    }}

    body {{
        font-family: Arial, sans-serif;
        background: white;
        color: #222;
        margin: 0;
        padding: 10px;
    }}

    .recibo {{
        width: 100%;
        background: white;
        padding: 18px;
        border: 2px solid #28713b;
        border-radius: 8px;
    }}

    .encabezado {{
        text-align: center;
        border-bottom: 2px solid #28713b;
        padding-bottom: 10px;
        margin-bottom: 12px;
    }}

    .mata {{
        font-size: 65px;
        line-height: 1.1;
    }}

    .logo {{
        color: #17632f;
        font-size: 34px;
        font-weight: bold;
        margin: 2px;
    }}

    .titulo {{
        font-size: 19px;
        font-weight: bold;
    }}

    .seccion {{
        color: #17632f;
        font-weight: bold;
        font-size: 14px;
        margin: 12px 0 7px;
    }}

    table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 12px;
    }}

    th {{
        background: #e5efe5;
        color: #17632f;
        text-align: left;
    }}

    td, th {{
        border: 1px solid #cbd8cb;
        padding: 6px;
    }}

    .datos td {{
        width: 50%;
    }}

    .numero {{
        text-align: right;
    }}

    .total {{
        background: #e4f1e4;
        border: 2px solid #28713b;
        text-align: center;
        padding: 12px;
        margin-top: 13px;
    }}

    .total h2 {{
        color: #17632f;
        font-size: 25px;
        margin: 5px;
    }}

    .firmas {{
        display: flex;
        justify-content: space-around;
        gap: 30px;
        margin-top: 35px;
        text-align: center;
        font-size: 11px;
    }}

    .firma {{
        width: 45%;
        border-top: 1px solid #555;
        padding-top: 6px;
    }}

    .pie {{
        text-align: center;
        margin-top: 18px;
        color: #17632f;
        font-weight: bold;
        font-size: 13px;
    }}

    .botones {{
        display: flex;
        gap: 8px;
        margin-top: 12px;
    }}

    .botones button {{
        flex: 1;
        padding: 12px 5px;
        border: none;
        border-radius: 6px;
        color: white;
        font-weight: bold;
        background: #28713b;
        cursor: pointer;
    }}

    .botones button:last-child {{
        background: #555;
    }}

    @media print {{
        body {{
            padding: 0;
        }}

        .recibo {{
            border: 1px solid #28713b;
            padding: 10px;
        }}

        .botones {{
            display: none !important;
        }}

        * {{
            print-color-adjust: exact;
            -webkit-print-color-adjust: exact;
        }}
    }}

    </style>
    </head>

    <body>

    <div class="recibo" id="recibo">

        <div class="encabezado">
            <div class="mata">🌾</div>
            <div class="logo">RAFC</div>
            <div class="titulo">LIQUIDACION DE ARROZ</div>
            <small>RECIBO DE COMPRA Y RECEPCION</small>
        </div>

        <div class="seccion">DATOS GENERALES</div>

        <table class="datos">
            <tr>
                <td><b>Productor:</b> {productor}</td>
                <td><b>Comprador:</b> {comprador}</td>
            </tr>
            <tr>
                <td><b>Variedad:</b> {variedad}</td>
                <td><b>Año de cosecha:</b> {datos["anio"]}</td>
            </tr>
            <tr>
                <td colspan="2"><b>Fecha:</b> {fecha_texto}</td>
            </tr>
        </table>

        <div class="seccion">DETALLES DE LIQUIDACION</div>

        <table>
            <tr><th>Concepto</th><th>Resultado</th></tr>

            <tr><td>Total de sacos</td>
                <td class="numero">{datos["sacos"]:,}</td></tr>

            <tr><td>Peso bruto</td>
                <td class="numero">{datos["bruto"]:,.2f} kg</td></tr>

            <tr><td>Descuento por saco</td>
                <td class="numero">0.50 kg</td></tr>

            <tr><td>Descuento total</td>
                <td class="numero">{datos["descuento"]:,.2f} kg</td></tr>

            <tr><td>Peso neto</td>
                <td class="numero">{datos["neto"]:,.2f} kg</td></tr>

            <tr><td>Humedad</td>
                <td class="numero">{datos["humedad"]}%</td></tr>

            <tr><td>Divisor calculado</td>
                <td class="numero">{datos["divisor"]}</td></tr>

            <tr><td>Rendimiento</td>
                <td class="numero">{datos["rendimiento"]:,.4f} fanegas</td></tr>

            <tr><td>Precio por fanega</td>
                <td class="numero">RD$ {datos["precio"]:,.2f}</td></tr>

            <tr><td>Precio por saco</td>
                <td class="numero">RD$ {datos["precio_saco"]:,.2f}</td></tr>
        </table>

        <div class="total">
            <b>TOTAL A PAGAR</b>
            <h2>RD$ {datos["total"]:,.2f}</h2>
        </div>

        <div class="firmas">
            <div class="firma">Firma del productor</div>
            <div class="firma">Firma del comprador</div>
        </div>

        <div class="pie">
            Created by RAFC 2026
        </div>

    </div>

    <div class="botones">
        <button onclick="descargarPNG()">📸 Descargar PNG</button>
        <button onclick="window.print()">🖨️ Imprimir A4</button>
    </div>

    <script>

    function descargarPNG() {{

        const elemento = document.getElementById("recibo");

        html2canvas(elemento, {{
            scale: 2,
            backgroundColor: "#ffffff"
        }}).then(canvas => {{

            const enlace = document.createElement("a");

            enlace.download = "liquidacion_RAFC.png";
            enlace.href = canvas.toDataURL("image/png");
            enlace.click();

        }});

    }}

    </script>

    </body>
    </html>
    """


# ==================================================
# FUNCION: LIQUIDACION DE ARROZ
# ==================================================

def pantalla_liquidacion():

    st.markdown(
        '<div class="titulo-rafc">🌾 RAFC</div>',
        unsafe_allow_html=True
    )

    st.subheader("Liquidacion de Arroz")

    st.markdown("### Datos generales")

    productor = st.text_input("Nombre del productor")

    comprador = st.text_input("Nombre del comprador")

    variedad = st.text_input("Variedad de arroz")

    anio = st.number_input(
        "Año de cosecha",
        min_value=0,
        value=0,
        step=1
    )

    fecha = st.date_input(
        "Fecha de liquidacion",
        value=date.today()
    )

    st.markdown("---")
    st.markdown("### Datos de peso y rendimiento")

    total_sacos = st.number_input(
        "Total de sacos",
        min_value=0,
        value=0,
        step=1
    )

    peso_bruto = st.number_input(
        "Peso bruto (kg)",
        min_value=0.0,
        value=0.0,
        step=10.0
    )

    st.info("Descuento fijo por saco: 0.50 kg")

    humedad = st.number_input(
        "Humedad (%) - Numero entero",
        min_value=0,
        value=0,
        step=1,
        format="%d"
    )

    precio_fanega = st.number_input(
        "Precio por fanega (RD$)",
        min_value=0.0,
        value=0.0,
        step=50.0
    )

    # ----------------------------------------------
    # CALCULAR
    # ----------------------------------------------

    if st.button(
        "CALCULAR LIQUIDACION",
        type="primary",
        use_container_width=True
    ):

        if total_sacos <= 0:
            st.error("Debes introducir el total de sacos.")
            st.session_state.resultado = None

        elif peso_bruto <= 0:
            st.error("Debes introducir el peso bruto.")
            st.session_state.resultado = None

        elif not productor.strip():
            st.error("Debes introducir el nombre del productor.")
            st.session_state.resultado = None

        elif not comprador.strip():
            st.error("Debes introducir el nombre del comprador.")
            st.session_state.resultado = None

        elif not variedad.strip():
            st.error("Debes introducir la variedad del arroz.")
            st.session_state.resultado = None

        elif anio <= 0:
            st.error("Debes introducir el año de cosecha.")
            st.session_state.resultado = None

        elif precio_fanega <= 0:
            st.error("Debes introducir el precio por fanega.")
            st.session_state.resultado = None

        else:

            descuento = total_sacos * TARA_FIJA

            peso_neto = peso_bruto - descuento

            divisor = 100 + int(humedad)

            if peso_neto <= 0:
                st.error(
                    "El peso neto debe ser mayor que cero. "
                    "Revisa el peso bruto y los sacos."
                )
                st.session_state.resultado = None

            else:

                rendimiento = peso_neto / divisor

                total = rendimiento * precio_fanega

                precio_saco = total / total_sacos

                st.session_state.resultado = {
                    "productor": productor,
                    "comprador": comprador,
                    "variedad": variedad,
                    "anio": int(anio),
                    "fecha": fecha,
                    "sacos": int(total_sacos),
                    "bruto": peso_bruto,
                    "descuento": descuento,
                    "neto": peso_neto,
                    "humedad": int(humedad),
                    "divisor": divisor,
                    "rendimiento": rendimiento,
                    "precio": precio_fanega,
                    "precio_saco": precio_saco,
                    "total": total
                }

    # ----------------------------------------------
    # MOSTRAR RESULTADO
    # ----------------------------------------------

    datos = st.session_state.resultado

    if datos is not None:

        st.markdown("---")
        st.markdown("### Resultado de la liquidacion")

        st.success(
            f"TOTAL A PAGAR: RD$ {datos['total']:,.2f}"
        )

        st.write(f"Descuento total: {datos['descuento']:,.2f} kg")

        st.write(f"Peso neto: {datos['neto']:,.2f} kg")

        st.write(f"Divisor calculado: {datos['divisor']}")

        st.write(
            f"Rendimiento: {datos['rendimiento']:,.4f} fanegas"
        )

        st.write(
            f"Precio por saco: RD$ {datos['precio_saco']:,.2f}"
        )

        # Recibo HTML, vista previa, impresion y PNG
        recibo_html = crear_recibo(datos)

        components.html(
            recibo_html,
            height=1050,
            scrolling=True
        )

        # Descargar TXT
        texto_txt = f"""
RAFC - LIQUIDACION DE ARROZ

Productor: {datos['productor']}
Comprador: {datos['comprador']}
Variedad: {datos['variedad']}
Año de cosecha: {datos['anio']}
Fecha: {datos['fecha'].strftime('%d/%m/%Y')}

DETALLES DE LIQUIDACION

Total de sacos: {datos['sacos']}
Peso bruto: {datos['bruto']:.2f} kg
Descuento por saco: 0.50 kg
Descuento total: {datos['descuento']:.2f} kg
Peso neto: {datos['neto']:.2f} kg
Humedad: {datos['humedad']}%
Divisor calculado: {datos['divisor']}
Rendimiento: {datos['rendimiento']:.4f} fanegas
Precio por fanega: RD$ {datos['precio']:.2f}
Precio por saco: RD$ {datos['precio_saco']:.2f}

TOTAL A PAGAR: RD$ {datos['total']:.2f}

Created by RAFC 2026
"""

        st.download_button(
            "📥 Descargar liquidacion TXT",
            data=texto_txt,
            file_name="liquidacion_RAFC.txt",
            mime="text/plain",
            use_container_width=True
        )

    st.markdown("---")

    if st.button("⬅ Volver al menu principal"):
        st.session_state.pagina = "inicio"
        st.rerun()


# ==================================================
# CONTROL PRINCIPAL DE PANTALLAS
# ==================================================

if st.session_state.pagina == "inicio":

    pantalla_inicio()

elif st.session_state.pagina == "liquidacion":

    pantalla_liquidacion()

elif st.session_state.pagina == "calculadora":

    calculadora_general()
