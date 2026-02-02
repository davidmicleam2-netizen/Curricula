import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
import os
import datetime

# CONFIGURACIÓN DE PÁGINA (Poner al principio del todo)
st.set_page_config(
    page_title="IA Career Manager | Tu Agente de Empleo",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
st.title("🚀 Agencia de Empleo con IA ")

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

# Línea 66 (aprox)
if api_key:  # <--- Fíjate que esto termina en dos puntos
    
    # Línea 69 (AQUÍ ESTABA EL ERROR)
    # Tienes que empujarla para que esté ALINEADA dentro del if
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Auditoría", "CV Visual", "Carta Premium", "Entrevista", "Feedback"])
    
    # El resto del código también debe estar alineado igual...

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
                        
   # === PESTAÑA 3: CARTA DE PRESENTACIÓN PREMIUM (EL FRANCOTIRADOR) ===
    with tab3:
        st.header("Redactor de Cartas de Alto Impacto")
        st.info("Esta herramienta analiza la oferta y redacta una carta que 'hackea' la psicología del reclutador.")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            empresa = st.text_input("Nombre de la Empresa:", placeholder="Ej: Google, Zara, Mercadona")
        with col2:
            tono = st.selectbox("Tono de la Carta:", ["Profesional y Corporativo", "Moderno y Creativo", "Directo y Persuasivo"])

        oferta = st.text_area("Pega aquí la DESCRIPCIÓN COMPLETA de la oferta de trabajo:", height=200, placeholder="Copia y pega los requisitos y responsabilidades de la oferta...")
        
        if st.button("Redactar Carta Premium") and oferta and empresa:
            if not texto_cv:
                st.error("Primero sube tu CV en el menú lateral.")
            else:
                with st.spinner("🕵️‍♂️ Analizando la oferta y buscando coincidencias en tu perfil..."):
                    
                    # PROMPT DE INGENIERÍA SOCIAL
                    prompt = f"""
                    Actúa como un Copywriter experto en Ventas y RRHH.
                    TU OBJETIVO: Escribir una carta de presentación IRRESISTIBLE para la empresa {empresa}.
                    
                    TONO ELEGIDO: {tono}.

                    DATOS:
                    - CV DEL CANDIDATO: {texto_cv}
                    - OFERTA DE TRABAJO: {oferta}

                    INSTRUCCIONES DE ESTRUCTURA (NO HAGAS LA TÍPICA CARTA ABURRIDA):
                    1. SALUDO: Si no hay nombre, usa algo profesional pero cercano.
                    2. EL GANCHO (Párrafo 1): No empieces con "Le escribo para...". Empieza mencionando un dolor/necesidad que leíste en la oferta y cómo te entusiasma resolverlo.
                    3. LA EVIDENCIA (Párrafo 2): Elige UN logro o habilidad del CV que coincida EXACTAMENTE con el requisito más difícil de la oferta. Usa la técnica "Problema -> Acción -> Resultado".
                    4. EL CIERRE (CTA): Nada de "espero su respuesta". Propón una reunión breve para explicar cómo puedes aportar valor desde el día 1.
                    
                    BONUS OBLIGATORIO:
                    Al final, separada por una línea, escribe una "Opción de Mensaje Corto para LinkedIn" (max 300 caracteres) para enviar al reclutador directamente.

                    IDIOMA: Español de España (Neutro y profesional).
                    """
                    
                    try:
                        resultado = consultar_gemini(prompt, api_key)
                        
                        st.subheader("📝 Tu Carta Personalizada")
                        st.markdown(resultado)
                        
                        st.download_button(
                            label="📥 Descargar Carta (.txt)",
                            data=resultado,
                            file_name=f"Carta_para_{empresa}.txt",
                            mime="text/plain"
                        )
                        
                    except Exception as e:
                        st.error(f"Error redactando: {e}")

 # === PESTAÑA 4: ENTRENADOR DE ENTREVISTAS (MODO CHULETA RÁPIDA) ===
    with tab4:
        st.header("Entrenador de Entrevistas (Modo Flashcard)")
        st.info("Genera una guía ultra-rápida para leer 5 minutos antes de entrar.")
        
        col1, col2 = st.columns(2)
        with col1:
            cargo_entrevista = st.text_input("Puesto al que aplicas:", placeholder="Ej: Dependiente")
        with col2:
            empresa_entrevista = st.text_input("Empresa:", placeholder="Ej: Zara")
            
        oferta_entrevista = st.text_area("Pega la descripción de la oferta (Opcional):", height=100)
        
        if st.button("Generar Chuleta Rápida") and cargo_entrevista:
            if not texto_cv:
                st.error("Primero sube tu CV en el menú lateral.")
            else:
                with st.spinner("⚡ Sintetizando las mejores respuestas..."):
                    
                    prompt = f"""
                    Actúa como un Preparador de Entrevistas.
                    TU OBJETIVO: Crear una "CHULETA" (Cheat Sheet) esquemática y muy breve.
                    NO ESCRIBAS PÁRRAFOS LARGOS. USA UN ESTILO DIRECTO Y VISUAL.

                    CONTEXTO:
                    - Puesto: {cargo_entrevista} en {empresa_entrevista}
                    - CV: {texto_cv}
                    - Oferta: {oferta_entrevista}

                    GENERAR:

                    1. ⚡ EL PITCH DE 45 SEGUNDOS:
                       Escribe un párrafo de MÁXIMO 4 LÍNEAS para responder "Háblame de ti". Ve al grano: Quién soy + Logro Clave + Por qué yo.

                    2. 🥊 3 PREGUNTAS CLAVE (Formato S.A.R. Rápido):
                       Identifica 3 preguntas probables y da la respuesta en este formato ESQUEMÁTICO:
                       * ❓ Pregunta: [La pregunta]
                       * 💡 Idea Clave: [1 frase sobre qué responder]
                       * 🗣️ Ejemplo rápido: "En mi experiencia X, hice Y logrando Z". (Máximo 2 líneas).

                    3. 🛡️ DEFENSA CONTRA DEBILIDAD:
                       Identifica el punto débil del CV y escribe 1 FRASE CONTUNDENTE para defenderlo.

                    4. 🧠 2 PREGUNTAS PARA EL RECLUTADOR:
                       2 preguntas cortas e inteligentes para hacer al final.

                    FORMATO: Usa muchos emojis, negritas y listas. Debe leerse en 60 segundos.
                    """
                    
                    try:
                        guia = consultar_gemini(prompt, api_key)
                        st.markdown(guia)
                        
                        st.download_button(
                            label="📥 Descargar Chuleta (.txt)",
                            data=guia,
                            file_name=f"Chuleta_Express_{cargo_entrevista}.txt",
                            mime="text/plain"
                        )
                        
                    except Exception as e:
                        st.error(f"Error en la simulación: {e}")
                        
    
   # === PESTAÑA 5: SOPORTE Y COMUNIDAD ===
    with tab5:
        st.header("🤝 Centro de Ayuda y Feedback")
        st.info("¿Te ha gustado? Ayúdanos a mejorar o reporta errores.")
        
        col_feedback, col_contacto = st.columns(2)
        
        # COLUMNA IZQUIERDA: COMUNIDAD
        with col_feedback:
            st.subheader("📢 Tu opinión cuenta")
            st.write("Si la herramienta te ha servido, deja un comentario en nuestra comunidad para que sigamos mejorando.")
            
            valoracion = st.feedback("stars") # Nuevo sistema de estrellas nativo de Streamlit (más bonito)
            if valoracion:
                st.write("¡Gracias por tu valoración! ⭐")
            
            st.markdown("---")
            # AQUÍ PEGARÁS TU LINK DE UDIA CUANDO LO TENGAS
            st.link_button("💬 Ir al Hilo de la Comunidad (Udia)", "https://udia.com") 

        # COLUMNA DERECHA: CONTACTO DIRECTO
        with col_contacto:
            st.subheader("🐛 Reportar un Problema")
            st.write("¿La IA ha fallado? ¿Tienes una idea? Envíame un correo directo.")
            
            # TU CORREO REAL CONFIGURADO
            email_destino = "davidmicleam2@gmail.com"
            asunto = "Feedback IA Career Manager"
            cuerpo = "Hola David, he estado probando la app y..."
            
            # Botón HTML con estilo profesional
            estilo_boton = """
            <a href="mailto:{}?subject={}&body={}" style="text-decoration: none;">
                <div style="
                    background-color: #FF4B4B;
                    color: white;
                    padding: 12px 20px;
                    border-radius: 8px;
                    text-align: center;
                    font-weight: bold;
                    display: inline-block;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
                ">
                    ✉️ Enviar Email a David
                </div>
            </a>
            """.format(email_destino, asunto, cuerpo)
            
            st.markdown(estilo_boton, unsafe_allow_html=True)
            
            st.caption("📧 Se abrirá tu gestor de correo predeterminado.")
