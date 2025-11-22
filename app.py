import streamlit as st
import unicodedata
import re

# Configuración de la página
st.set_page_config(
    page_title="Ordenador de Textos Poéticos",
    page_icon="📖",
    layout="wide"
)

# Título y descripción
st.title("📖 Ordenador de Textos Poéticos")
st.markdown("""
Esta aplicación ordena alfabéticamente las líneas de textos poéticos.
Puedes **subir un archivo** o **pegar el texto directamente**.
""")

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

# Tabs para diferentes métodos de entrada
tab1, tab2 = st.tabs(["📁 Subir Archivo", "✍️ Pegar Texto"])

texto_procesado = None

with tab1:
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

with tab2:
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
st.markdown("""
<div style='text-align: center'>
    <p>💡 <strong>Tip:</strong> Esta herramienta ordena las líneas alfabéticamente, 
    ignorando acentos y considerando mayúsculas/minúsculas según tus preferencias.</p>
</div>
""", unsafe_allow_html=True)
