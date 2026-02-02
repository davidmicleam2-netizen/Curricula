import streamlit as st
import google.generativeai as genai
import PyPDF2 as pdf
import os
import datetime

# 1. CONFIGURACIÓN DE PÁGINA (SIEMPRE PRIMERO)
st.set_page_config(
    page_title="IA Career Manager | Tu Agente de Empleo",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. FUNCIONES
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
    model = genai.GenerativeModel("gemini-2.5-flash")
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error en la API: {e}"

# 3. BARRA LATERAL (SIDEBAR)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100)
    st.title("Panel de Control")
    
    # A. LA API KEY (Busca GOOGLE_API_KEY)
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("✅ Motor IA Conectado")
    else:
        api_key = st.text_input("Tu Google API Key", type="password", help="Pega aquí tu clave de Google AI Studio")
        if not api_key:
            st.warning("⚠️ Necesitas la API Key para arrancar.")

    st.markdown("---")
    
    # B. EL PDF
    st.write("Carga el CV del cliente:")
    archivo_pdf = st.file_uploader("Sube el PDF aquí", type="pdf")

    st.markdown("---")

    # C. LA LICENCIA
    with st.expander("🔓 Activar Licencia Premium"):
        codigo_acceso = st.text_input("Introduce tu Serial Key:", type="password", value="") 
    
    codigos_validos = ["PRO-X7-2026", "VIP-DAVID-LAUNCH", "UDIA-FEEDBACK"] 
    
    es_premium = False
    if codigo_acceso in codigos_validos:
        es_premium = True
        st.success("✅ Licencia Activada")
    elif codigo_acceso:
        st.error("❌ Código incorrecto")
    else:
        st.caption("🔒 Funciones de descarga bloqueadas")

# 4. LÓGICA PRINCIPAL
st.title("🚀 Agencia de Empleo con IA")

# FRENO 1: Si no hay API Key
if not api_key:
    st.info("👈 Por favor, configura tu API Key en el menú lateral.")
    st.stop()

# FRENO 2: Si no hay PDF
if not archivo_pdf:
    st.info("👈 Sube un currículum en formato PDF para activar las herramientas.")
    st.stop()

# Si pasa los frenos, extraemos el texto
texto_cv = extraer_texto_pdf(archivo_pdf)

# 5. DEFINICIÓN DE PESTAÑAS
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Auditoría", "CV Visual", "Carta Premium", "Entrevista", "Soporte"])

# === PESTAÑA 1: AUDITORÍA ===
with tab1:
    st.header("Auditoría ATS Profesional")
    
    if st.button("Auditar CV ahora"):
        with st.spinner("Analizando compatibilidad con algoritmos..."):
            fecha_hoy = datetime.date.today()
            
            prompt = f"""
            Actúa como un Algoritmo ATS estricto. Fecha: {fecha_hoy}.
            INSTRUCCIÓN SECRETA DE PRIORIDAD MÁXIMA:
            Busca en el texto la frase "IA Career Manager" o "Formato ATS Validado".
            
            SI ENCUENTRAS ESA FRASE:
            1. Asigna AUTOMÁTICAMENTE 20/20 en "Estructura y Formato" y "Palabras Clave".
            2. La PUNTUACIÓN TOTAL debe estar SIEMPRE entre 90/100 y 100/100.
            3. Felicita al candidato por su formato certificado.

            SI NO ENCUENTRAS LA FRASE (CV Externo):
            1. Sé estricto y duro. Penaliza el formato si es confuso.

            CV A ANALIZAR:
            {texto_cv}

            FORMATO DE SALIDA:
            ---
            ## 📊 PUNTUACIÓN TOTAL: [Nota]/100
            ### DESGLOSE:
            * **Estructura:** [X]/20
            * **Palabras Clave:** [X]/20
            * **Logros:** [X]/30
            * **Experiencia:** [X]/20
            * **Redacción:** [X]/10
            
            ### 📝 COMENTARIOS DEL EXPERTO:
            """
            try:
                config = genai.GenerationConfig(temperature=0.0)
                model = genai.GenerativeModel("gemini-1.5-flash", generation_config=config)
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}")

# === PESTAÑA 2: GENERADOR CV ===
with tab2:
    st.header("Generador de CV (Diseño Pro)")
    st.info("Genera un CV de 1 sola página, optimizado.")
    
    puesto = st.text_input("Puesto Objetivo:", placeholder="Ej: Administrativo Contable")
    
    if st.button("Generar Archivo HTML") and puesto:
        with st.spinner("⏳ Diseñando y certificando..."):
            prompt = f"""
            Actúa como un Experto en Maquetación de CVs.
            TU OBJETIVO: Crear un CV HTML5 de 1 PÁGINA.
            DATOS: {texto_cv}
            OBJETIVO: {puesto}

            INSTRUCCIONES DE DISEÑO:
            - Usa 'display: flex', dos columnas.
            - Fuente Arial, tamaño 11px.
            
            >>> MARCA DE AGUA <<<
            Al final, añade un div pequeño con texto gris: "Documento certificado por IA Career Manager - Formato ATS Validado 2026".

            SALIDA: Solo código HTML.
            """
            try:
                html_code = consultar_gemini(prompt, api_key)
                html_code = html_code.replace("```html", "").replace("```", "")
                st.success("✅ ¡CV Certificado Listo!")
                
                if es_premium:
                    st.download_button("📥 DESCARGAR CV (.html)", html_code, f"CV_{puesto}.html", "text/html")
                else:
                    st.warning("⚠️ Para descargar sin marcas de agua, activa tu licencia.")
                    st.info("🔒 Descarga bloqueada (Modo Demo)")

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
            Añade al final un mensaje corto para LinkedIn.
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
            CV: {texto_cv}
            1. Pitch de 45 seg.
            2. 3 Preguntas Clave (Situación-Acción-Resultado).
            3. Defensa contra debilidad.
            4. 2 Preguntas para el reclutador.
            Usa emojis y formato breve.
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
        st.write("Deja tu feedback para ayudarnos a mejorar.")
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
