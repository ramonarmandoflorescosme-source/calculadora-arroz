import streamlit as str_lit
import streamlit.components.v1 as components
from datetime import date, datetime
from html import escape
import json
from PIL import Image
import pillow_heif
from google import genai
from google.genai import types

# Habilitar soporte para .HEIC de iPhone/Samsung
pillow_heif.register_heif_opener()

str_lit.set_page_config(
    page_title="Liquidación de Arroz",
    page_icon="🌾",
    layout="centered"
)

# ==================================
# CONFIGURACIÓN DE IA EN BARRA LATERAL
# ==================================
with str_lit.sidebar:
    str_lit.header("⚙️ Configuración de Escaneo")
    api_key = str_lit.text_input("Tu API Key de Gemini:", type="password", help="Necesaria para leer las fotos de facturas reales automáticamente.")
    str_lit.caption("Ingresa tu API key para activar la lectura de la foto.")

str_lit.title("🌾 LIQUIDADORA DE ARROZ")
str_lit.write("Sistema de cálculo y control con escaneo inteligente de recibos oficiales.")
str_lit.markdown("---")

# ==================================
# FUNCIÓN DE LECTURA DE FACTURA (IA)
# ==================================
def analizar_factura_arroz(imagen_pil, clave_api):
    client = genai.Client(api_key=clave_api)
    
    prompt = """
    Eres un experto leyendo facturas manuscritas de 'PESADA DE ARROZ EN CASCARA' en República Dominicana.
    Analiza esta imagen y extrae los siguientes datos en formato JSON estricto:
    {
        "numero_recibo": "string (el número rojo/impreso arriba a la derecha, ej: 12616)",
        "productor": "string (nombre en 'Recibido de:', ej: Ramon Flores)",
        "fecha": "string en formato YYYY-MM-DD (ej: 2025-03-25)",
        "variedad": "string (ej: Jurero)",
        "pesadas_kilos": [lista de números float/int con TODOS los kilos anotados en las columnas de 'KILOS' de izquierda a derecha, leyendo fila por fila],
        "total_sacos": int (número en el cuadro de 'Sacos', ej: 118, o 0 si no está escrito),
        "humedad_factor": float (número escrito en 'Humedad:', ej: 123.0, o 130.0 si está vacío),
        "precio_fanega": float (si está escrito en 'Fanega:', sino 3600.0)
    }
    Asegúrate de leer con cuidado los números escritos a lápiz o lapicero en las columnas de KILOS. No inventes números si una casilla está vacía.
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[imagen_pil, prompt],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.1
        )
    )
    return json.loads(response.text)

# ==================================
# 1. OPCIÓN DE ESCANEO / FOTO DE RECIBO
# ==================================
str_lit.header("📸 Escaneo de Recibo / Cuaderno")
foto_recibo = str_lit.file_uploader(
    "Sube una foto de la factura oficial (JPG, PNG o HEIC):",
    type=["jpg", "jpeg", "png", "heic"]
)

# Valores por defecto
datos_ocr = {
    "numero_recibo": "",
    "productor": "",
    "fecha": date.today(),
    "variedad": "",
    "pesadas_kilos": [],
    "total_sacos": 0,
    "humedad_factor": 130.0,
    "precio_fanega": 3600.0
}

if foto_recibo is not None:
    try:
        imagen = Image.open(foto_recibo)
        with str_lit.expander("👁️ Ver foto cargada", expanded=False):
            str_lit.image(imagen, use_container_width=True)

        if api_key:
            if "ultima_foto" not in str_lit.session_state or str_lit.session_state["ultima_foto"] != foto_recibo.name:
                with str_lit.spinner("🔍 Leyendo factura manuscrita con IA... un momento..."):
                    resultado = analizar_factura_arroz(imagen, api_key)
                    str_lit.session_state["datos_extraidos"] = resultado
                    str_lit.session_state["ultima_foto"] = foto_recibo.name
                    str_lit.success("¡Factura leída con éxito! Revisa los datos abajo.")
                    str_lit.rerun()
        else:
            str_lit.warning("⚠️ **Falta la API Key:** Ingresala en la barra lateral izquierda (⚙️ Configuración de Escaneo) para que la IA lea la foto automáticamente.")
    except Exception as e:
        str_lit.error(f"Error procesando la imagen: {e}")

if "datos_extraidos" in str_lit.session_state:
    ext = str_lit.session_state["datos_extraidos"]
    datos_ocr["numero_recibo"] = str(ext.get("numero_recibo", ""))
    datos_ocr["productor"] = str(ext.get("productor", ""))
    datos_ocr["variedad"] = str(ext.get("variedad", ""))
    datos_ocr["pesadas_kilos"] = ext.get("pesadas_kilos", [])
    datos_ocr["total_sacos"] = int(ext.get("total_sacos", 0) or 0)
    datos_ocr["humedad_factor"] = float(ext.get("humedad_factor", 130.0) or 130.0)
    datos_ocr["precio_fanega"] = float(ext.get("precio_fanega", 3600.0) or 3600.0)
    try:
        if ext.get("fecha"):
            datos_ocr["fecha"] = datetime.strptime(ext["fecha"], "%Y-%m-%d").date()
    except ValueError:
        pass

str_lit.markdown("---")

# ==================================
# 2. DATOS DEL COMPRADOR Y RECIBO
# ==================================
str_lit.header("📋 Datos del recibo")

comprador = str_lit.text_input("Nombre del comprador:")
productor = str_lit.text_input("Nombre del productor:", value=datos_ocr["productor"])
molino = str_lit.text_input("Nombre del molino:")
numero_recibo = str_lit.text_input("Número de recibo:", value=datos_ocr["numero_recibo"])
fecha_recibo = str_lit.date_input("Fecha del recibo", value=datos_ocr["fecha"])
variedad = str_lit.text_input("Variedad de arroz:", value=datos_ocr["variedad"])

str_lit.markdown("---")

# ==================================
# 3. METODO DE ENTRADA DE PESO
# ==================================
str_lit.header("⚖️ Datos del peso")

indice_modo = 2 if len(datos_ocr["pesadas_kilos"]) > 0 else 0

modo = str_lit.radio(
    "Selecciona el método de entrada:",
    ["Peso Bruto Total (kg)", "Por Pesadas (Báscula)", "Lista de Pesadas Escaneadas"],
    index=indice_modo
)

if modo == "Peso Bruto Total (kg)":
    total_sacos = str_lit.number_input(
        "Total de sacos:",
        min_value=0,
        value=datos_ocr["total_sacos"],
        step=1
    )
    peso_bruto = str_lit.number_input(
        "Peso bruto total (kg):",
        min_value=0.0,
        value=float(sum(datos_ocr["pesadas_kilos"])) if datos_ocr["pesadas_kilos"] else 0.0,
        step=10.0
    )

elif modo == "Por Pesadas (Báscula)":
    num_pesadas = str_lit.number_input("Número de pesadas:", min_value=0, value=0, step=1)
    sacos_pesada = str_lit.number_input("Sacos por cada pesada:", min_value=0, value=0, step=1)
    kilos_pesada = str_lit.number_input("Kilos por pesada (kg):", min_value=0.0, value=0.0, step=10.0)

    total_sacos = num_pesadas * sacos_pesada
    peso_bruto = num_pesadas * kilos_pesada

else:
    str_lit.write("Verifica o corrige las pesadas individuales extraídas de las columnas:")
    
    texto_pesadas_default = ", ".join(map(str, datos_ocr["pesadas_kilos"])) if datos_ocr["pesadas_kilos"] else ""
    texto_pesadas = str_lit.text_area("Pesadas (separadas por comas):", value=texto_pesadas_default, height=120)
    
    try:
        lista_kilos = [float(k.strip()) for k in texto_pesadas.split(",") if k.strip()]
    except ValueError:
        lista_kilos = []
        str_lit.error("Por favor, introduce solo números válidos separados por comas.")

    sacos_default = datos_ocr["total_sacos"] if datos_ocr["total_sacos"] > 0 else len(lista_kilos) * 3
    total_sacos = str_lit.number_input(
        "Total de sacos:",
        min_value=0,
        value=sacos_default,
        step=1
    )
    
    peso_bruto = sum(lista_kilos)
    str_lit.info(f"👉 **Peso Bruto Sumado:** {peso_bruto:,.2f} kg | **Total de pesadas leídas:** {len(lista_kilos)}")

# ==================================
# 4. DATOS DE LIQUIDACION
# ==================================
str_lit.markdown("---")
str_lit.header("💰 Datos de liquidación")

tara_por_saco = str_lit.number_input(
    "Tara por saco (kg):",
    min_value=0.0,
    value=0.5,
    step=0.1
)

str_lit.caption("A menor factor divisor, mayor cantidad de fanegas.")
factor_divisor = str_lit.number_input(
    "Factor divisor / Humedad (Peso neto ÷ Factor):",
    min_value=1.0,
    value=datos_ocr["humedad_factor"],
    step=1.0
)

precio_fanega = str_lit.number_input(
    "Precio por fanega (RD$):",
    min_value=0.0,
    value=datos_ocr["precio_fanega"],
    step=100.0
)

observaciones = str_lit.text_area("Observaciones (ej. Humedad estimada, sacos vacíos, calidad del grano):")

# ==================================
# 5. CALCULAR LIQUIDACION
# ==================================
str_lit.markdown("---")

if str_lit.button("CALCULAR LIQUIDACIÓN", type="primary"):

    if "liquidacion" in str_lit.session_state:
        del str_lit.session_state["liquidacion"]

    if total_sacos <= 0 or peso_bruto <= 0:
        str_lit.warning("Ingresa una cantidad válida de sacos y peso bruto.")

    elif peso_bruto - (total_sacos * tara_por_saco) <= 0:
        str_lit.warning("El peso neto debe ser mayor que cero.")

    elif factor_divisor <= 0:
        str_lit.warning("El factor divisor debe ser mayor que cero.")

    else:
        tara_sacos = total_sacos * tara_por_saco
        peso_neto = peso_bruto - tara_sacos

        rendimiento_fanegas = peso_neto / factor_divisor
        etiqueta_factor = "Factor divisor / Humedad"
        valor_factor = f"{factor_divisor:.2f}"

        total_pagar = rendimiento_fanegas * precio_fanega
        precio_por_saco = total_pagar / total_sacos

        str_lit.session_state["liquidacion"] = {
            "comprador": comprador,
            "productor": productor,
            "molino": molino,
            "numero_recibo": numero_recibo,
            "fecha": fecha_recibo.strftime("%d/%m/%Y"),
            "hora_calculo": datetime.now().strftime("%I:%M:%S %p"),
            "variedad": variedad,
            "modo": modo,
            "total_sacos": total_sacos,
            "peso_bruto": peso_bruto,
            "tara_por_saco": tara_por_saco,
            "tara_sacos": tara_sacos,
            "peso_neto": peso_neto,
            "etiqueta_factor": etiqueta_factor,
            "valor_factor": valor_factor,
            "rendimiento": rendimiento_fanegas,
            "precio_fanega": precio_fanega,
            "total_pagar": total_pagar,
            "precio_por_saco": precio_por_saco,
            "observaciones": observaciones
        }

# ==================================
# 6. MOSTRAR RESULTADOS Y COMPROBANTE
# ==================================
if "liquidacion" in str_lit.session_state:

    datos = str_lit.session_state["liquidacion"]

    str_lit.markdown("---")
    str_lit.header("📊 RESULTADOS DE LA LIQUIDACIÓN")

    col1, col2 = str_lit.columns(2)
    with col1:
        str_lit.metric("Peso neto real", f"{datos['peso_neto']:,.2f} kg")
        str_lit.metric("Total a pagar", f"RD$ {datos['total_pagar']:,.2f}")
    with col2:
        str_lit.metric("Rendimiento", f"{datos['rendimiento']:,.4f} fanegas")
        str_lit.metric("Precio por saco", f"RD$ {datos['precio_por_saco']:,.2f}")

    str_lit.markdown("---")
    str_lit.header("🖨️ Comprobante de liquidación")

    d = datos
    observaciones_html = escape(d["observaciones"]).replace("\n", "<br>")
    num_recibo_limpio = escape(d["numero_recibo"].strip()) if d["numero_recibo"].strip() else "sin_numero"
    nombre_archivo = f"Liquidacion_Arroz_{num_recibo_limpio}.png"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <style>
        * {{ box-sizing: border-box; }}
        html, body {{ font-family: Arial, sans-serif; color: #222; margin: 0; padding: 0; background: transparent; }}
        .recibo {{ width: 100%; max-width: 700px; margin: 20px auto; background: #ffffff; border: 1px solid #999; padding: 20px 18px; font-size: 11px; }}
        h1, h2 {{ text-align: center; }}
        h1 {{ font-size: 19px; margin: 6px 0 4px 0; }}
        h2 {{ font-size: 15px; margin: 3px 0; }}
        h3 {{ font-size: 12px; margin: 8px 0 4px; }}
        .subtitulo {{ text-align: center; font-size: 11px; margin: 3px 0; }}
        .datos {{ line-height: 1.5; margin-top: 8px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 6px; }}
        th, td {{ border: 1px solid #999; padding: 5px; text-align: left; }}
        th {{ background: #eeeeee; }}
        .total {{ margin-top: 9px; padding: 10px; background: #eeeeee; font-size: 17px; font-weight: bold; text-align: right; }}
        .observaciones {{ margin-top: 9px; min-height: 20px; line-height: 1.4; overflow-wrap: anywhere; }}
        .firmas {{ display: flex; justifyContent: space-between; margin-top: 30px; gap: 30px; }}
        .firma {{ width: 50%; text-align: center; border-top: 1px solid #333; padding-top: 5px; }}
        .autor {{ text-align: center; font-size: 9px; font-weight: bold; letter-spacing: 1px; margin-top: 8px; }}
        .no-imprimir {{ display: flex; justify-content: center; flex-wrap: wrap; gap: 12px; margin-top: 15px; margin-bottom: 20px; }}
        .boton-accion {{ padding: 12px 22px; font-size: 15px; font-weight: bold; color: white; border: 0; border-radius: 6px; cursor: pointer; }}
        .boton-imprimir {{ background: #168342; }}
        .boton-descargar {{ background: #0d6efd; }}
    </style>
    </head>
    <body>
    <div class="recibo" id="comprobante-captura">
        <h1>🌾 LIQUIDADORA DE ARROZ</h1>
        <h2>COMPROBANTE DE CÁLCULO</h2>
        <p class="subtitulo">CONTROL DEL COMPRADOR</p>
        <hr>
        <div class="datos">
            <b>COMPRADOR:</b> {escape(d['comprador'])}<br>
            <b>PRODUCTOR:</b> {escape(d['productor'])}<br>
            <b>MOLINO:</b> {escape(d['molino'])}<br>
            <b>NÚMERO DE RECIBO:</b> {escape(d['numero_recibo'])}<br>
            <b>FECHA:</b> {escape(d['fecha'])} ({escape(d['hora_calculo'])})<br>
            <b>VARIEDAD DE ARROZ:</b> {escape(d['variedad'])}
        </div>
        <hr>
        <h3>DETALLE DE LA LIQUIDACIÓN</h3>
        <table>
            <tr><th>Concepto</th><th>Resultado</th></tr>
            <tr><td>Total de sacos</td><td>{d['total_sacos']}</td></tr>
            <tr><td>Peso bruto</td><td>{d['peso_bruto']:,.2f} kg</td></tr>
            <tr><td>Tara por saco</td><td>{d['tara_por_saco']:.2f} kg</td></tr>
            <tr><td>Descuento de tara</td><td>{d['tara_sacos']:,.2f} kg</td></tr>
            <tr><td>Peso neto</td><td>{d['peso_neto']:,.2f} kg</td></tr>
            <tr><td>{d['etiqueta_factor']}</td><td>{d['valor_factor']}</td></tr>
            <tr><td>Rendimiento</td><td>{d['rendimiento']:,.4f} fanegas</td></tr>
            <tr><td>Precio por fanega</td><td>RD$ {d['precio_fanega']:,.2f}</td></tr>
            <tr><td>Precio por saco</td><td>RD$ {d['precio_por_saco']:,.2f}</td></tr>
        </table>
        <div class="total">TOTAL A PAGAR: RD$ {d['total_pagar']:,.2f}</div>
        <div class="observaciones"><b>OBSERVACIONES:</b><br>{observaciones_html}</div>
        <div class="firmas">
            <div class="firma">Firma del comprador</div>
            <div class="firma">Firma de recibido</div>
        </div>
        <hr>
        <p class="subtitulo">Documento de control interno. No sustituye el recibo original.</p>
        <div class="autor">🌾 CREADA POR RAFC © 2026</div>
    </div>
    <div class="no-imprimir">
        <button class="boton-accion boton-imprimir" onclick="window.print()">🖨️ IMPRIMIR COMPROBANTE</button>
        <button id="btn-descargar" class="boton-accion boton-descargar" onclick="descargarImagen()">📥 DESCARGAR IMAGEN (PNG)</button>
    </div>
    <script>
        function descargarImagen() {{
            const btn = document.getElementById("btn-descargar");
            btn.innerHTML = "⏳ Generando imagen...";
            btn.disabled = true;
            html2canvas(document.getElementById("comprobante-captura"), {{ scale: 2, backgroundColor: "#ffffff", useCORS: true }}).then(canvas => {{
                const enlace = document.createElement("a");
                enlace.download = "{nombre_archivo}";
                enlace.href = canvas.toDataURL("image/png");
                enlace.click();
                btn.innerHTML = "📥 DESCARGAR IMAGEN (PNG)";
                btn.disabled = false;
            }});
        }}
    </script>
    </body>
    </html>
    """
    components.html(html, height=1080, scrolling=True)

str_lit.markdown("---")
str_lit.markdown(
    '<div style="text-align:center; color:gray; font-size:15px; font-weight:bold; letter-spacing:1px; padding:12px;">🌾 CREADA POR RAFC © 2026</div>',
    unsafe_allow_html=True
)

