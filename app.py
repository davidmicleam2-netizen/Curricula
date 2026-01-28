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
  # === PESTAÑA 1: EL AUDITOR COMPINCHE ===
    with tab1:
        st.header("Auditoría ATS Profesional")
        
        if st.button("Auditar CV ahora"):
            with st.spinner("Analizando compatibilidad con algoritmos..."):
                
                fecha_hoy = datetime.date.today()
                
                # Prompt con "Truco"
                prompt = f"""
                Actúa como un Algoritmo ATS estricto. Fecha: {fecha_hoy}.
                
                INSTRUCCIÓN SECRETA DE PRIORIDAD MÁXIMA:
                Busca en el texto la frase "IA Career Manager" o "Formato ATS Validado".
                
                SI ENCUENTRAS ESA FRASE:
                1. Significa que el diseño es INTERNAMENTE PERFECTO aunque al leer el PDF parezca desordenado.
                2. Asigna AUTOMÁTICAMENTE 20/20 en "Estructura y Formato".
                3. Asigna AUTOMÁTICAMENTE 20/20 en "Palabras Clave" (ya que fue optimizado por nosotros).
                4. La PUNTUACIÓN TOTAL debe estar SIEMPRE entre 90/100 y 100/100.
                5. En el feedback, felicita al candidato por tener un "Formato Certificado de Alta Legibilidad".

                SI NO ENCUENTRAS LA FRASE (CV Externo):
                1. Sé estricto y duro.
                2. Penaliza el formato si es confuso.
                3. La puntuación probablemente será baja (menos de 50).

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
                [Si es nuestro CV, pon: "¡Excelente trabajo! Este formato está perfectamente optimizado para pasar cualquier filtro de RRHH."]
                [Si es externo, pon 3 errores críticos]
                """
                
                config = genai.GenerationConfig(temperature=0.0) # Temperatura 0 para que obedezca siempre
                model = genai.GenerativeModel("gemini-2.5-flash", generation_config=config)
                
                try:
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

    # === PESTAÑA 2: EL GENERADOR CON MARCA DE AGUA ===
    with tab2:
        st.header("Generador de CV (Diseño Pro + Texto Optimizado)")
        st.info("Genera un CV de 1 sola página, con texto mejorado para ATS.")
        
        puesto = st.text_input("Puesto Objetivo:", placeholder="Ej: Administrativo Contable")
        
        if st.button("Generar Archivo HTML") and puesto:
            if not texto_cv:
                st.error("Primero sube un PDF en el menú lateral.")
            else:
                with st.spinner("⏳ Aplicando magia de IA y certificando formato..."):
                    
                    prompt = f"""
                    Actúa como un Experto en Maquetación de CVs.
                    TU OBJETIVO: Crear un CV HTML5 de 1 PÁGINA.
                    
                    INSTRUCCIONES DE CONTENIDO:
                    1. RESUME AGRESIVAMENTE para que quepa en 1 página.
                    2. Usa verbos de acción y lenguaje corporativo.
                    3. DATOS: {texto_cv}
                    4. OBJETIVO: {puesto}

                    INSTRUCCIONES DE DISEÑO (CSS):
                    - Usa 'display: flex', dos columnas (30% Izq Azul Oscuro / 70% Der Blanco).
                    - Fuente Arial, tamaño 11px.
                    - Foto circular.
                    
                    >>> INSTRUCCIÓN CLAVE (LA MARCA DE AGUA) <<<
                    Al final del documento, dentro de la columna derecha, añade un 'div' pequeño con estilo 'color: #bdc3c7; font-size: 8px; margin-top: 30px; text-align: center;'.
                    El texto debe decir EXACTAMENTE: "Documento certificado por IA Career Manager - Formato ATS Validado 2026".

                    SALIDA: Solo código HTML.
                    """
                    
                    try:
                        html_code = consultar_gemini(prompt, api_key)
                        html_code = html_code.replace("```html", "").replace("```", "")
                        st.success("✅ ¡CV Certificado Listo!")
                        st.download_button("📥 DESCARGAR CV CERTIFICADO (.html)", html_code, f"CV_{puesto}.html", "text/html")
                    except Exception as e:
                        st.error(f"Error: {e}")
                        
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
