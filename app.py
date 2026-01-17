import streamlit as st
import unicodedata
import re
import requests

# Configuración de la página
st.set_page_config(
    page_title="Ordenador de Textos Poéticos",
    page_icon="📖",
    layout="wide"
)

# CSS personalizado con paleta de colores verde suave y negro
st.markdown("""
<style>
    /* Color de fondo principal - verde suave */
    .stApp {
        background-color: #2d5016;
    }
    
    /* Texto principal - negro */
    .stMarkdown, p, span, div {
        color: #000000 !important;
    }
    
    /* Títulos - negro */
    h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
    }
    
    /* Botones - verde más oscuro con texto negro */
    .stButton > button {
        background-color: #4a7c2c;
        color: #000000;
        border: 2px solid #3d6623;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background-color: #5a8c3c;
        border-color: #4a7c2c;
    }
    
    /* Inputs y text areas - fondo verde claro */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #3d6623;
        color: #000000;
        border: 1px solid #2d5016;
    }
    
    /* Tabs - tonos verdes */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #2d5016;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #000000;
        background-color: #3d6623;
        border: 1px solid #2d5016;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #4a7c2c;
        color: #000000;
    }
    
    /* Sidebar - verde oscuro */
    [data-testid="stSidebar"] {
        background-color: #1f3a10;
    }
    
    /* Cajas de información */
    .stAlert {
        background-color: #3d6623;
        border: 1px solid #2d5016;
        color: #000000;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #3d6623;
        color: #000000 !important;
        border: 1px solid #2d5016;
    }
    
    /* Checkboxes */
    .stCheckbox label {
        color: #000000 !important;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background-color: #3d6623;
        border: 1px solid #2d5016;
    }
    
    /* Métricas */
    [data-testid="stMetricValue"] {
        color: #000000 !important;
    }
    
    /* Links - verde más oscuro */
    a {
        color: #1f3a10 !important;
        font-weight: bold;
    }
    
    a:hover {
        color: #2d5016 !important;
    }
    
    /* Spinner y elementos de carga */
    .stSpinner > div {
        border-top-color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# Logo y título
col1, col2 = st.columns([1, 4])
with col1:
    st.image("logo.png", width=150)
with col2:
    st.title("📖 Ordenador de Textos Poéticos")

st.markdown("""
Suele decirse (con mucha razón) que la vanguardia está muerta. Sin embargo, hay textos y autores que buscan dialogar con el fantasma de la vanguardia (como diría Tabarobsky). Uno de esos textos es el "Martín Fierro ordenado alfabéticamente" y uno de esos autores es Pablo Katchadjian: toma el Martín Fierro (la ida) y reescribirlo sin agregar nada: simplemente ordena de forma alfabética los versos y lo publica. El libro es pura forma. Pero no pura forma del lenguaje (que también lo es): es puro procedimiento, puro artefacto. Y como tal es reproducible. ¿Qué otros textos podríamos ordenar alfabéticamente? Toda la gauchesca, desde ya. La poesía épica, dada su extensión, parece bastante adecuada.

Esta app busca hacer replicable y escalable el procedimiento de Katchadjian. Ordena alfabéticamente las líneas de textos poéticos.
Se puede **cargar desde URL**, **subir un archivo** o **pegar el texto directamente**.
""")

# Imagen del Martín Fierro ordenado
try:
    col_img1, col_img2, col_img3 = st.columns([1, 1, 1])
    with col_img2:
        st.image("mf_ordenado.jpg", caption="Martín Fierro ordenado alfabéticamente - Pablo Katchadjian", use_container_width=True)
except:
    pass  # Si no está la imagen, no rompe la app

# Función para normalizar texto para ordenamiento
def normalize_for_sorting(s):
    """Normaliza el texto eliminando acentos para el ordenamiento"""
    return unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode('utf-8').lower()

# Función para procesar el texto
def procesar_texto(texto, filtrar_numeros=True, capitalizar=True, eliminar_guiones=True):
    """
    Procesa el texto y devuelve las líneas ordenadas alfabéticamente
    """
    # Dividir en líneas
    lineas = texto.splitlines()
    lineas_procesadas = []
    
    # Lista de prefijos que indican numeración romana
    numeros_romanos = [
        "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", 
        "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX"
    ]
    
    for linea in lineas:
        linea = linea.strip()
        
        # Filtrar líneas vacías
        if not linea:
            continue
            
        # Filtrar numeración si está activado
        if filtrar_numeros:
            if linea.isdigit():
                continue
            if linea.startswith("Cap"):
                continue
            if any(linea.startswith(num) for num in numeros_romanos):
                continue
        
        # Corregir signos iniciales y formatear texto
        if capitalizar:
            if linea.startswith("!"):
                linea = "¡" + linea[1:]
            if linea[0] in ".,;:!?¡¿":
                linea = linea[0] + linea[1:].capitalize()
            else:
                linea = linea[:1].upper() + linea[1:].lower()
        
        # Eliminar guiones si está activado
        if eliminar_guiones:
            linea = linea.replace("-", "")
        
        lineas_procesadas.append(linea)
    
    # Ordenar alfabéticamente
    lineas_ordenadas = sorted(lineas_procesadas, key=normalize_for_sorting)
    
    return lineas_ordenadas

# Sidebar con opciones
st.sidebar.header("⚙️ Opciones de Procesamiento")
filtrar_numeros = st.sidebar.checkbox("Filtrar números y numeración romana", value=True)
capitalizar = st.sidebar.checkbox("Capitalizar primera letra", value=True)
eliminar_guiones = st.sidebar.checkbox("Eliminar guiones", value=True)

# Información adicional en sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("""
### 👨‍💻 Desarrollador
<a href="https://gefero.github.io/" target="_blank" style="text-decoration: none; color: #000000;">
    <strong>gefero.github.io</strong>
</a>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
### 🏢 Institución
<a href="https://factor-data.netlify.app/" target="_blank" style="text-decoration: none; color: #000000;">
    <strong>factor~data EIDAES_UNSAM</strong>
</a>
""", unsafe_allow_html=True)

# Tabs para diferentes métodos de entrada
tab1, tab2, tab3 = st.tabs(["🔗 Desde URL", "📁 Subir Archivo", "✍️ Pegar Texto"])

texto_procesado = None

with tab1:
    st.subheader("Descarga desde un enlace")
    st.markdown("Introduce la URL de un archivo .txt para procesarlo")
    
    url_input = st.text_input(
        "URL del archivo",
        placeholder="https://www.gutenberg.org/cache/epub/14765/pg14765.txt",
        help="Ingresa la URL completa del archivo de texto"
    )
    
    # Opciones avanzadas para textos desde URL
    with st.expander("⚙️ Opciones avanzadas (opcional)"):
        usar_delimitadores = st.checkbox(
            "Usar delimitadores de inicio y fin",
            value=False,
            help="Extrae solo el texto entre dos frases específicas"
        )
        
        if usar_delimitadores:
            col1, col2 = st.columns(2)
            with col1:
                inicio_texto = st.text_input(
                    "Texto de inicio",
                    placeholder="Aquí me pongo a cantar",
                    help="Frase donde comienza el texto a extraer"
                )
            with col2:
                fin_texto = st.text_input(
                    "Texto de fin",
                    placeholder="Pero que naides conteste",
                    help="Frase donde termina el texto a extraer"
                )
    
    if url_input:
        if st.button("🔄 Descargar y ordenar desde URL", key="btn_url"):
            try:
                with st.spinner("Descargando archivo desde la URL..."):
                    # Descargar el texto desde la URL
                    response = requests.get(url_input, timeout=30)
                    response.raise_for_status()
                    texto = response.text
                    
                    st.success(f"✅ Archivo descargado correctamente ({len(texto)} caracteres)")
                    
                    # Si se usan delimitadores, extraer solo esa parte
                    if usar_delimitadores and inicio_texto and fin_texto:
                        patron = re.escape(inicio_texto) + ".*" + re.escape(fin_texto)
                        match = re.search(patron, texto, re.DOTALL)
                        if match:
                            texto = match.group(0)
                            st.info(f"📝 Texto extraído entre delimitadores ({len(texto)} caracteres)")
                        else:
                            st.warning("⚠️ No se encontraron los delimitadores. Se procesará todo el texto.")
                    
                    # Mostrar preview del texto original
                    with st.expander("👁️ Ver texto descargado"):
                        preview = texto[:1000] + "..." if len(texto) > 1000 else texto
                        st.text_area("Texto original (preview)", preview, height=200, disabled=True)
                    
                    # Procesar
                    with st.spinner("Procesando texto..."):
                        texto_procesado = procesar_texto(texto, filtrar_numeros, capitalizar, eliminar_guiones)
                        
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Error al descargar el archivo: {str(e)}")
                st.info("Verifica que la URL sea correcta y que el servidor esté disponible.")
            except Exception as e:
                st.error(f"❌ Error al procesar el archivo: {str(e)}")

with tab2:
    st.subheader("Sube tu archivo de texto")
    uploaded_file = st.file_uploader(
        "Selecciona un archivo .txt",
        type=['txt'],
        help="Sube un archivo de texto con tu poema o texto"
    )
    
    if uploaded_file is not None:
        # Leer el archivo
        texto = uploaded_file.read().decode('utf-8')
        st.success(f"✅ Archivo cargado: {uploaded_file.name}")
        
        # Mostrar preview del texto original
        with st.expander("👁️ Ver texto original"):
            st.text_area("Texto original", texto, height=200, disabled=True)
        
        # Procesar
        if st.button("🔄 Ordenar texto del archivo", key="btn_file"):
            with st.spinner("Procesando..."):
                texto_procesado = procesar_texto(texto, filtrar_numeros, capitalizar, eliminar_guiones)

with tab3:
    st.subheader("Pega tu texto aquí")
    texto_input = st.text_area(
        "Escribe o pega tu texto poético",
        height=300,
        placeholder="Aquí me pongo a cantar\nAl compás de la vigüela...",
        help="Pega el texto que deseas ordenar alfabéticamente"
    )
    
    if texto_input:
        if st.button("🔄 Ordenar texto pegado", key="btn_text"):
            with st.spinner("Procesando..."):
                texto_procesado = procesar_texto(texto_input, filtrar_numeros, capitalizar, eliminar_guiones)

# Mostrar resultados
if texto_procesado:
    st.success(f"✅ Procesamiento completado: {len(texto_procesado)} líneas ordenadas")
    
    # Crear dos columnas para mostrar resultados y estadísticas
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("📝 Texto Ordenado Alfabéticamente")
        resultado_texto = "\n".join(texto_procesado)
        st.text_area(
            "Resultado",
            resultado_texto,
            height=400,
            help="Texto ordenado alfabéticamente"
        )
    
    with col2:
        st.subheader("📊 Estadísticas")
        st.metric("Total de líneas", len(texto_procesado))
        
        # Mostrar primeras letras más comunes
        primeras_letras = {}
        for linea in texto_procesado:
            if linea:
                letra = linea[0].upper()
                primeras_letras[letra] = primeras_letras.get(letra, 0) + 1
        
        st.write("**Líneas por letra inicial:**")
        for letra, cantidad in sorted(primeras_letras.items())[:10]:
            st.write(f"{letra}: {cantidad}")
    
    # Botón de descarga
    st.download_button(
        label="⬇️ Descargar texto ordenado",
        data=resultado_texto,
        file_name="texto_ordenado.txt",
        mime="text/plain",
        help="Descarga el texto ordenado como archivo .txt"
    )

# Footer
st.markdown("---")
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
    <div style='text-align: center'>
        <p>💡 <strong>Tip:</strong> Esta herramienta ordena las líneas alfabéticamente, 
        ignorando acentos y considerando mayúsculas/minúsculas según tus preferencias.</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div style='text-align: center'>
        <p><small>Desarrollado por<br>
        <strong><a href="https://gefero.github.io/" target="_blank" style="text-decoration: none; color: #000000;">gefero</a></strong><br>
        <strong><a href="https://factor-data.netlify.app/" target="_blank" style="text-decoration: none; color: #000000;">factor~data EIDAES_UNSAM</a></strong></small></p>
    </div>
    """, unsafe_allow_html=True)
