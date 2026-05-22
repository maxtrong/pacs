import streamlit as st
import cv2
import numpy as np
import pydicom
from PIL import Image, ImageOps
import time

# Configuración visual v7.1
st.set_page_config(page_title="MAXTRONG PACS v7.1", layout="wide")

# CSS para imitar CustomTkinter (Negro y Gris Médico)
st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a; color: white; }
    [data-testid="stSidebar"] { background-color: #2b2b2b; border-right: 1px solid #3d3d3d; }
    .stButton>button { background-color: #3d3d3d; color: white; border-radius: 5px; height: 3em; width: 100%; border: 1px solid #555; }
    .stButton>button:hover { background-color: #17a2b8; border-color: #17a2b8; }
    </style>
    """, unsafe_allow_html=True)

# Splash Screen Materializado (3 segundos)
if 'pacs_load' not in st.session_state:
    holder = st.empty()
    with holder.container():
        st.write("##")
        try:
            st.image("maxtrong_pacs.png", use_container_width=True)
        except:
            st.title("MAXTRONG PACS 2026")
        time.sleep(3)
    st.session_state.pacs_load = True
    holder.empty()

# Estructura de 3 Columnas original
col_pacientes, col_visor, col_herramientas = st.columns([1, 3, 1])

with col_pacientes:
    st.subheader("📁 ESTUDIOS")
    archivo = st.file_uploader("Cargar DICOM", type=["dcm", "jpg", "png"], label_visibility="collapsed")
    st.markdown("---")
    if archivo:
        st.button(f"👤 {archivo.name}", type="secondary")

with col_visor:
    st.markdown("<div style='background-color:black; padding:10px; border-radius:10px; border:2px solid #333;'>", unsafe_allow_html=True)
    if archivo:
        if archivo.name.lower().endswith('.dcm'):
            ds = pydicom.dcmread(archivo)
            img = ds.pixel_array.astype(float)
            img_base = np.uint8((np.maximum(img,0) / img.max()) * 255.0)
        else:
            file_bytes = np.asarray(bytearray(archivo.read()), dtype=np.uint8)
            img_base = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
        
        # Inversión automática v7.1
        img_final = cv2.bitwise_not(img_base)
        st.image(img_final, use_container_width=True)
    else:
        st.image(np.zeros((600, 800), dtype=np.uint8), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_herramientas:
    st.subheader("🛠️ TOOLS")
    st.button("🔍 LUPA")
    st.button("📏 REGLA")
    st.markdown("---")
    st.write("☀️ Brillo")
    st.slider("B", -100, 100, 0, label_visibility="collapsed")
    st.write("◑ Contraste")
    st.slider("C", 0.5, 3.0, 1.0, label_visibility="collapsed")
    if st.button("📝 INFORME", type="primary"):
        st.success("Módulo de informe listo.")
