import streamlit as st
import google.generativeai as genai
import PyPDF2 as pdf
import os
import datetime
import base64
import requests

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="IA Career Manager | Tu Agente de Empleo",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. FUNCIONES AUXILIARES
def extraer_texto_pdf(uploaded_file):
    try:
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in range(len(reader.pages)):
            text += str(reader.pages[page].extract_text())
        return text
    except Exception as e:
        st.error(f"Error leyendo el PDF: {e}")
        return None

def consultar_gemini(prompt, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error en la API: {e}"

# 3. BARRA LATERAL (SIDEBAR)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100)
    st.title("Panel de Control")
    
    # A. API KEY
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("✅ Motor IA Conectado")
    else:
        api_key = st.text_input("Tu Google API Key", type="password", help="Pega tu clave aquí")
        if not api_key:
            st.warning("⚠️ Necesitas la API Key para arrancar.")

    st.markdown("---")

    # B. LICENCIA (ARRIBA)
    with st.expander("🔓 Activar Licencia Premium", expanded=True):
        codigo_acceso = st.text_input("Introduce tu Serial Key:", type="password", value="") 
    
    # Lógica de Validación (Simple + Gumroad ready)
    es_premium = False
    codigos_comunidad = ["PRO-X7-2026", "VIP-DAVID-LAUNCH", "UDIA-FEEDBACK"]
    
    if codigo_acceso in codigos_comunidad:
        es_premium = True
        st.success("✅ Licencia Activada (Comunidad)")
    elif codigo_acceso:
        st.error("❌ Código incorrecto")
    else:
        st.caption("🔒 Modo Demo (Descargas bloqueadas)")

    st.markdown("---")
    
    # C. CARGA DE ARCHIVOS
    st.write("📁 **Archivos del Candidato:**")
    archivo_pdf = st.file_uploader("1. Sube el CV (PDF)", type="pdf")
    archivo_foto = st.file_uploader("2. Foto de perfil (Opcional)", type=["jpg", "jpeg", "png"])

# 4. LÓGICA PRINCIPAL
st.title("🚀 Agencia de Empleo con IA")

# FRENOS DE SEGURIDAD
if not api_key:
    st.info("👈 Configura tu API Key en el menú lateral.")
    st.stop()

if not archivo_pdf:
    st.info("👈 Sube un currículum PDF para empezar.")
    st.stop()

# Si todo ok, leemos el PDF
texto_cv = extraer_texto_pdf(archivo_pdf)

# 5. PESTAÑAS DE HERRAMIENTAS
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Auditoría", "CV Visual", "Carta Premium", "Entrevista", "Soporte"])

# === PESTAÑA 1: AUDITORÍA ===
with tab1:
    st.header("Auditoría ATS Profesional")
    if st.button("Auditar CV ahora"):
        with st.spinner("Analizando compatibilidad con algoritmos..."):
            fecha_hoy = datetime.date.today()
            prompt = f"""
            Actúa como un Algoritmo ATS estricto. Fecha: {fecha_hoy}.
            Busca en el texto la frase "IA Career Manager".
            SI LA ENCUENTRAS: Puntuación > 90/100.
            SI NO: Sé estricto.
            CV: {texto_cv}
            Genera un informe con Puntuación Total, Desglose y 3 Consejos de mejora.
            """
            try:
                res = consultar_gemini(prompt, api_key)
                st.markdown(res)
            except Exception as e:
                st.error(f"Error: {e}")

# === PESTAÑA 2: GENERADOR CV (VERSIÓN 5 - DISEÑO EQUILIBRADO) ===
with tab2:
    st.header("Generador de CV (Diseño Pro)")
    st.info("Genera un CV estético que llena la página correctamente.")
    puesto = st.text_input("Puesto Objetivo:", placeholder="Ej: Administrativo Contable")
    
    if st.button("Generar Archivo HTML") and puesto:
        with st.spinner("⏳ Diseñando con espaciado profesional..."):
            
            # Procesar Foto
            etiqueta_foto = ""
            if archivo_foto is not None:
                try:
                    bytes_foto = archivo_foto.getvalue()
                    b64_foto = base64.b64encode(bytes_foto).decode('utf-8')
                    mime_type = archivo_foto.type 
                    etiqueta_foto = f'<img src="data:{mime_type};base64,{b64_foto}" alt="Foto" style="display:block; width:170px; height:170px; object-fit:cover; border-radius:50%; border:5px solid white; margin: 30px auto 30px auto; box-shadow: 0 5px 15px rgba(0,0,0,0.3);">'
                except:
                    etiqueta_foto = '<div style="width:170px; height:170px; background:#bdc3c7; border-radius:50%; margin: 30px auto;"></div>'
            else:
                etiqueta_foto = '<div style="width:170px; height:170px; background:#bdc3c7; border-radius:50%; margin: 30px auto; display:flex; align-items:center; justify-content:center; font-size:50px; color:white; border:5px solid white;">👤</div>'

            prompt = f"""
            Actúa como un Diseñador Editorial Senior.
            OBJETIVO: CV de 1 PÁGINA (A4) que se vea LLENO, ORDENADO y PROFESIONAL.
            DATOS: {texto_cv}
            PUESTO: {puesto}

            CSS OBLIGATORIO:
            @page {{ margin: 0; size: A4; }}
            html, body {{ margin: 0; padding: 0; background: #f4f4f4; font-family: 'Helvetica', sans-serif; }}
            .a4-container {{ width: 210mm; min-height: 297mm; margin: 0 auto; background: white; display: flex; }}
            .col-left {{ width: 32%; background-color: #1e272e; color: white; padding: 30px 20px; text-align: center; display: flex; flex-direction: column; gap: 20px; }}
            .col-right {{ width: 68%; padding: 40px 35px; color: #333; display: flex; flex-direction: column; gap: 25px; }}
            h1 {{ font-size: 28px; margin: 0; color: #2c3e50; text-transform: uppercase; }}
            h2 {{ font-size: 16px; color: #e67e22; border-bottom: 2px solid #e67e22; padding-bottom: 5px; margin-bottom: 10px; text-transform: uppercase; }}
            
            ESTRUCTURA HTML:
            Columna Izquierda: [[FOTO_AQUI]], Contacto, Habilidades, Idiomas.
            Columna Derecha: Nombre (h1), Puesto, Perfil, Experiencia (Bullet points detallados), Educación.
            
            SALIDA: Solo código HTML.
            """

            try:
                html_code = consultar_gemini(prompt, api_key)
                html_code = html_code.replace("```html", "").replace("```", "")
                
                if "[[FOTO_AQUI]]" in html_code:
                    html_code = html_code.replace("[[FOTO_AQUI]]", etiqueta_foto)
                else:
                    html_code = etiqueta_foto + html_code

                st.success("✅ CV Generado")
                if es_premium:
                    st.download_button("📥 DESCARGAR CV (.html)", html_code, f"CV_{puesto}.html", "text/html")
                else:
                    st.warning("⚠️ Activa tu licencia para descargar.")
            except Exception as e:
                st.error(f"Error: {e}")

# === PESTAÑA 3: CARTA PREMIUM ===
with tab3:
    st.header("Redactor de Cartas")
    col1, col2 = st.columns([1, 1])
    with col1:
        empresa = st.text_input("Empresa:", placeholder="Ej: Google")
    with col2:
        tono = st.selectbox("Tono:", ["Profesional", "Creativo", "Directo"])

    oferta = st.text_area("Descripción de la oferta:", height=150)
    
    if st.button("Redactar Carta") and oferta and empresa:
        with st.spinner("✍️ Escribiendo..."):
            prompt = f"""
            Escribe una carta de presentación para {empresa} con tono {tono}.
            Usa el CV: {texto_cv} y la Oferta: {oferta}.
            Estructura: Gancho emocional, Evidencia de logros, Cierre con llamada a la acción.
            """
            try:
                resultado = consultar_gemini(prompt, api_key)
                st.markdown(resultado)
                if es_premium:
                    st.download_button("📥 Descargar Carta", resultado, f"Carta_{empresa}.txt")
                else:
                    st.warning("🔒 Descarga bloqueada")
            except Exception as e:
                st.error(f"Error: {e}")

# === PESTAÑA 4: ENTREVISTA ===
with tab4:
    st.header("Entrenador de Entrevistas")
    col1, col2 = st.columns(2)
    with col1:
        cargo_ent = st.text_input("Puesto:", placeholder="Ej: Dependiente")
    with col2:
        empresa_ent = st.text_input("Empresa (Entrevista):", placeholder="Ej: Zara")
        
    if st.button("Generar Chuleta") and cargo_ent:
        with st.spinner("🧠 Preparando estrategia..."):
            prompt = f"""
            Crea una "CHULETA" (Cheat Sheet) esquemática para entrevista de {cargo_ent} en {empresa_ent}.
            CV: {texto_cv}.
            1. Pitch 45s. 2. Preguntas Clave. 3. Debilidades. 4. Preguntas al reclutador.
            """
            try:
                guia = consultar_gemini(prompt, api_key)
                st.markdown(guia)
                if es_premium:
                    st.download_button("📥 Descargar Guía", guia, f"Guia_{cargo_ent}.txt")
                else:
                    st.warning("🔒 Descarga bloqueada")
            except Exception as e:
                st.error(f"Error: {e}")

# === PESTAÑA 5: SOPORTE ===
with tab5:
    st.header("🤝 Centro de Ayuda")
    st.info("¿Te ha gustado? Ayúdanos a mejorar.")
    col_feed, col_cont = st.columns(2)
    
    with col_feed:
        st.subheader("📢 Comunidad")
        val = st.feedback("stars")
        if val:
            st.write("¡Gracias! ⭐")
        st.link_button("💬 Ir a la Comunidad (Udia)", "https://udia.com") 

    with col_cont:
        st.subheader("🐛 Reportar Bug")
        email_destino = "davidmicleam2@gmail.com"
        asunto = "Feedback IA Career Manager"
        cuerpo = "Hola David, he encontrado un error..."
        
        estilo = """
        <a href="mailto:{}?subject={}&body={}" style="text-decoration: none;">
            <div style="background-color: #FF4B4B; color: white; padding: 10px; border-radius: 8px; text-align: center;">
                ✉️ Enviar Email a David
            </div>
        </a>
        """.format(email_destino, asunto, cuerpo)
        st.markdown(estilo, unsafe_allow_html=True)
