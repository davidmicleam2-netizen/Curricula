import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
import os
import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="IA Career Manager", page_icon="🚀", layout="wide")

# --- FUNCIONES ---
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

def consultar_gemini(prompt, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error en la API: {e}"

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100)
    st.title("Panel de Control")
    
   # 1. Buscamos la clave en los 'Secretos'
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("✅ Licencia Activada")  # <--- Fíjate que está alineado con la línea de arriba
    else:
        # 2. Si estamos en local
        api_key = st.text_input("Tu Google API Key", type="password")
        if not api_key:
            st.warning("⚠️ Introduce la clave para continuar.")

    st.markdown("---")
    st.write("Carga el CV del cliente:")
    archivo_pdf = st.file_uploader("Sube el PDF aquí", type="pdf")

# --- LÓGICA PRINCIPAL (EL CEREBRO) ---
st.title("🚀 Agencia de Empleo con IA - Girona")

# 1. FRENO DE SEGURIDAD: Si no hay clave, paramos aquí.
if not api_key:
    st.info("👈 Por favor, configura tu API Key en el menú lateral.")
    st.stop() # <--- ESTO EVITA EL ERROR

# 2. FRENO DE SEGURIDAD: Si no hay PDF, paramos aquí.
if not archivo_pdf:
    st.info("👈 Sube un currículum en formato PDF para activar las herramientas.")
    st.stop() # <--- ESTO EVITA EL ERROR "tab1 not defined"

# 3. SI LLEGAMOS AQUÍ, ES QUE TODO ESTÁ BIEN
texto_cv = extraer_texto_pdf(archivo_pdf)

if texto_cv:
    # Definimos las pestañas
    tab1, tab2, tab3, tab4 = st.tabs(["🕵️ Auditoría", "📄 CV Visual", "✉️ Carta Premium", "🎤 Entrevistas"])

 # === PESTAÑA 1: AUDITORÍA (MODO JUEZ ESTRICTO) ===
    with tab1:
        st.header("Auditoría ATS Profesional")
        st.info("Este sistema evalúa el CV con criterios objetivos de mercado.")
        
        if st.button("Auditar CV ahora"):
            with st.spinner("Aplicando rúbrica de evaluación estandarizada..."):
                
                # FECHA ACTUAL PARA EL CÁLCULO DE EDAD
                fecha_hoy = datetime.date.today()

                # CONFIGURACIÓN: Temperatura 0 para eliminar la aleatoriedad
                config_auditor = genai.GenerationConfig(
                    temperature=0.0,
                    top_p=1.0,
                    max_output_tokens=1000,
                )

                prompt = f"""
                Actúa como un Algoritmo ATS (Applicant Tracking System) estricto y objetivo.
                Fecha actual: {fecha_hoy}.
                
                TU TAREA: Evaluar este CV basándote EXCLUSIVAMENTE en la siguiente RÚBRICA DE PUNTUACIÓN (Total 100 puntos):

                1. ESTRUCTURA Y FORMATO (Máx 20 pts):
                   - ¿Es legible? ¿Tiene secciones claras? ¿Usa viñetas?
                2. PALABRAS CLAVE Y SEO (Máx 20 pts):
                   - ¿Menciona tecnologías o habilidades duras específicas del sector?
                3. IMPACTO Y LOGROS (Máx 30 pts):
                   - ¿Usa verbos de acción? ¿Hay métricas/números (%, €)? (Si solo lista tareas, penaliza mucho).
                4. EXPERIENCIA Y COHERENCIA (Máx 20 pts):
                   - ¿Las fechas tienen sentido según la fecha actual ({fecha_hoy.year})? ¿Hay lagunas sin explicar?
                5. ORTOGRAFÍA Y REDACCIÓN (Máx 10 pts):
                   - Penaliza errores gramaticales o frases vacías.

                CV DEL CANDIDATO:
                {texto_cv}

                FORMATO DE SALIDA REQUERIDO:
                ---
                ## 📊 PUNTUACIÓN TOTAL: [SUMA DE PUNTOS]/100
                
                ### DESGLOSE:
                * **Estructura:** [X]/20
                * **Palabras Clave:** [X]/20
                * **Logros:** [X]/30
                * **Experiencia:** [X]/20
                * **Redacción:** [X]/10
                
                ### 🚨 3 ERRORES CRÍTICOS DETECTADOS:
                1. [Error 1]
                2. [Error 2]
                3. [Error 3]

                ### 💡 EL CONSEJO DE ORO:
                [Una frase directa sobre qué cambiar ya mismo para subir nota]
                """
                
                # Usamos el modelo configurado con temperatura 0
                model = genai.GenerativeModel("gemini-1.5-flash", generation_config=config_auditor)
                try:
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error en el análisis: {e}")

    # === PESTAÑA 2: CV VISUAL ===
    with tab2:
        st.header("Diseño en 1 Cara")
        puesto = st.text_input("Puesto Objetivo:")
        if st.button("Generar HTML") and puesto:
            with st.spinner("Diseñando..."):
                prompt = f"Crea un CV HTML5 moderno de UNA SOLA CARA para {puesto} usando: {texto_cv}. Solo código HTML."
                html = consultar_gemini(prompt, api_key).replace("```html", "").replace("```", "")
                st.components.v1.html(html, height=800, scrolling=True)
                st.download_button("Descargar HTML", html, "cv.html", "text/html")

    # === PESTAÑA 3: CARTA ===
    with tab3:
        st.header("Carta de Presentación")
        oferta = st.text_area("Pega la oferta aquí:")
        if st.button("Redactar Carta") and oferta:
            with st.spinner("Escribiendo..."):
                prompt = f"Escribe carta de presentación uniendo este CV: {texto_cv} con esta oferta: {oferta}"
                carta = consultar_gemini(prompt, api_key)
                st.markdown(carta)

    # === PESTAÑA 4: ENTREVISTA ===
    with tab4:
        st.header("Entrenador de Entrevistas")
        if st.button("Generar Preguntas"):
            with st.spinner("Pensando preguntas difíciles..."):
                prompt = f"Genera 3 preguntas de entrevista difíciles basadas en las debilidades de este CV: {texto_cv}"
                res = consultar_gemini(prompt, api_key)
                st.markdown(res)
