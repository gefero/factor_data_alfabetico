# 📖 Ordenador de Textos Poéticos

Aplicación web interactiva para ordenar alfabéticamente las líneas de textos poéticos.

## 🚀 Características

- **Subir archivos**: Carga archivos .txt con tus poemas
- **Pegar texto**: Escribe o pega directamente el texto en la aplicación
- **Opciones personalizables**:
  - Filtrar números y numeración romana
  - Capitalizar primera letra de cada línea
  - Eliminar guiones
- **Ordenamiento inteligente**: Ignora acentos al ordenar para un resultado más natural
- **Descarga**: Exporta el texto ordenado como archivo .txt
- **Estadísticas**: Visualiza la distribución de líneas por letra inicial

## 📦 Instalación Local

1. Clona o descarga este repositorio
2. Asegúrate de tener el archivo `logo.png` en el mismo directorio que `app.py`
3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecuta la aplicación:
```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 🌐 Deploy en Streamlit Cloud

### Opción 1: Deploy desde GitHub

1. Sube los archivos (`app.py`, `requirements.txt` y `logo.png`) a un repositorio de GitHub

2. Ve a [share.streamlit.io](https://share.streamlit.io)

3. Haz clic en "New app"

4. Completa los datos:
   - **Repository**: Tu repositorio de GitHub
   - **Branch**: main (o la rama que uses)
   - **Main file path**: app.py

5. Haz clic en "Deploy"

### Opción 2: Deploy directo

1. Crea una cuenta gratuita en [Streamlit Cloud](https://streamlit.io/cloud)

2. Conecta tu cuenta de GitHub

3. Sigue los pasos de la Opción 1

## 📝 Uso

1. **Elige tu método de entrada**:
   - Pestaña "Subir Archivo": Carga un archivo .txt
   - Pestaña "Pegar Texto": Escribe o pega el texto directamente

2. **Ajusta las opciones** en la barra lateral según tus preferencias

3. **Haz clic en "Ordenar texto"**

4. **Visualiza el resultado** y las estadísticas

5. **Descarga** el texto ordenado con el botón de descarga

## 🛠️ Tecnologías

- **Streamlit**: Framework para la interfaz web
- **Python**: Lenguaje de programación
- **unicodedata**: Para normalización de caracteres

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso libre.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si encuentras algún error o tienes sugerencias, por favor abre un issue o pull request.

---

Desarrollado con ❤️ para amantes de la poesía
