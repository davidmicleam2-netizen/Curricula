import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
import os

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="IA Career Manager", page_icon="🚀", layout="wide")

# --- FUNCIÓN: EXTRACTOR DE PDF ---
def extraer_texto_pdf(uploaded_file):
    try:
        reader = PdfReader(uploaded_file)
        texto = ""
        for page in reader.pages:
            texto += page.extract_text() + "\n"
        return texto
    except Exception as e:
        st.error(f"Error leyendo el PDF: {e}")
        return None

# --- FUNCIONES DE IA (Gemini) ---
def consultar_gemini(prompt, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error en la API: {e}"

# --- INTERFAZ GRÁFICA (SIDEBAR) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100)
    st.title("Panel de Control")
    
    # --- GESTIÓN DE LA API KEY (MÉTODO SECRETO) ---
    # 1. Buscamos la clave en los 'Secretos' de la nube (invisible para el cliente)
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["AIzaSyAnhMnFYHcmdgGOZ54RESD3Ur9Mk3S6Hkc"]
        st.success("✅ Licencia Activada (Servidor)")
    else:
        # 2. Si estamos en tu ordenador local y no hay secretos, la pedimos manual
        api_key = st.text_input("Tu Google API Key", type="password")
        if not api_key:
            st.warning("⚠️ Introduce la clave para continuar.")

    st.markdown("---")
    st.write("Carga el CV del cliente:")
    archivo_pdf = st.file_uploader("Sube el PDF aquí", type="pdf")

    # === SERVICIO 1: AUDITORÍA ===
    with tab1:
        st.header("Auditoría ATS Implacable")
        if st.button("Analizar CV"):
            with st.spinner("El reclutador virtual está juzgando el CV..."):
                prompt = f"""
                Actúa como un Reclutador Experto. Analiza este CV:
                {texto_cv}
                Dame un informe con:
                1. PUNTUACIÓN (0-100).
                2. 🚨 3 ERRORES CRÍTICOS.
                3. 💡 FRASE DE VENTA para convencerle de contratar el servicio.
                """
                resultado = consultar_gemini(prompt, api_key)
                st.markdown(resultado)

    # === SERVICIO 2: CV VISUAL ===
    with tab2:
        st.header("Generador de CV Visual (Una Cara)")
        puesto_objetivo = st.text_input("Puesto Objetivo:", placeholder="Ej: Administrativo Contable")
        
        if st.button("Generar Diseño HTML"):
            if not puesto_objetivo:
                st.error("Indica el puesto objetivo.")
            else:
                with st.spinner("Diseñando y maquetando..."):
                    prompt = f"""
                    Crea un CV HTML5 profesional, moderno y CONDENSADO EN UNA SOLA CARA.
                    Diseño doble columna (Izquierda oscura / Derecha blanca).
                    Usa estos datos: {texto_cv}
                    Objetivo: {puesto_objetivo}
                    REGLA: Resume descripciones largas. SALIDA: Solo código HTML limpio.
                    """
                    html_code = consultar_gemini(prompt, api_key).replace("```html", "").replace("```", "")
                    
                    # Mostrar vista previa
                    st.components.v1.html(html_code, height=800, scrolling=True)
                    
                    # Botón de descarga
                    st.download_button(
                        label="Descargar HTML para imprimir",
                        data=html_code,
                        file_name="cv_optimizado.html",
                        mime="text/html"
                    )

    # === SERVICIO 3: CARTA DE PRESENTACIÓN ===
    with tab3:
        st.header("Redactor de Cartas de Presentación")
        oferta_trabajo = st.text_area("Pega aquí la descripción de la oferta de trabajo:")
        
        if st.button("Redactar Carta"):
            if len(oferta_trabajo) < 10:
                st.warning("Pega una oferta real.")
            else:
                with st.spinner("Conectando puntos..."):
                    prompt = f"""
                    Escribe una Carta de Presentación conectando este CV: {texto_cv}
                    Con esta Oferta: {oferta_trabajo}
                    Tono: Persuasivo y profesional.
                    """
                    carta = consultar_gemini(prompt, api_key)
                    st.markdown(carta)
                    st.download_button("Descargar Carta (.txt)", carta, "carta.txt")

    # === SERVICIO 4: ENTREVISTA (NUEVO) ===
    with tab4:
        st.header("Entrenador de Entrevistas (Simulador)")
        st.info("Genera las preguntas más difíciles que le harán basadas en SU experiencia.")
        
        if st.button("Generar Simulacro de Entrevista"):
            with st.spinner("Analizando debilidades del perfil..."):
                prompt = f"""
                Actúa como un Jefe de Recursos Humanos duro. Basado en este CV:
                {texto_cv}
                
                Genera una GUÍA DE PREPARACIÓN que incluya:
                1. 👺 LA PREGUNTA TRAMPA: La pregunta más difícil basada en sus debilidades (ej: huecos temporales, poca experiencia).
                2. 🎯 CÓMO RESPONDERLA: Un guion sugerido usando la técnica STAR.
                3. ❓ 3 PREGUNTAS TÉCNICAS: Específicas de su sector.
                4. 🧠 PREGUNTA PSICOLÓGICA: Para evaluar su encaje cultural.
                """
                entrevista = consultar_gemini(prompt, api_key)
                st.markdown(entrevista)
                st.download_button("Descargar Guía de Entrevista", entrevista, "guia_entrevista.txt")