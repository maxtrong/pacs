# -*- coding: utf-8 -*-
import streamlit as st
import cv2
import numpy as np
import pydicom
from PIL import Image, ImageOps, ImageDraw
from datetime import datetime
import io
import time
from docx import Document

# 1. CONFIGURACIÓN E INYECCIÓN DE ESTILO (Para imitar v7.1)
st.set_page_config(page_title="MAXTRONG PACS V7.1", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Fondo oscuro total */
    .stApp { background-color: #1a1a1a; color: #ffffff; }
    
    /* Paneles laterales imitando CustomTkinter */
    [data-testid="stSidebar"] {
        background-color: #2b2b2b;
        border-right: 2px solid #3d3d3d;
        min-width: 300px !important;
    }
    
    /* Botones cuadrados y grises de la v7.1 */
    .stButton>button {
        background-color: #3d3d3d;
        color: white;
        border-radius: 8px;
        border: 1px solid #555;
        height: 60px;
        font-weight: bold;
        font-size: 18px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #17a2b8; /* El azul que usábamos en la v7.1 */
        border-color: #17a2b8;
    }
    
    /* Contenedor del Visor */
    .visor-container {
        background-color: #000000;
        border: 2px solid #3d3d3d;
        border-radius: 12px;
        padding: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. SISTEMA DE SPLASH SCREEN (FADE-IN MATERIALIZADO)
if 'pacs_ready' not in st.session_state:
    placeholder = st.empty()
    with placeholder.container():
        cols = st.columns([1, 2, 1])
        with cols[1]:
            st.write("##") # Espaciado
            try:
                img_logo = Image.open("maxtrong_pacs.png")
                st.image(img_logo, use_container_width=True)
            except:
                st.header("MAXTRONG PACS 2026")
            st.markdown("<h3 style='text-align: center; color: #17a2b8;'>Iniciando Estación Radiológica...</h3>", unsafe_allow_html=True)
            time.sleep(3.5)
    st.session_state.pacs_ready = True
    placeholder.empty()

# 3. INTERFAZ PRINCIPAL (Distribución idéntica a v7.1)
col_izq, col_centro, col_der = st.columns([1, 3, 1])

# --- COLUMNA IZQUIERDA: PACIENTES ---
with col_izq:
    st.markdown("### 📂 ESTUDIOS")
    subir = st.file_uploader("IMPORTAR", type=["dcm", "jpg", "png"], label_visibility="collapsed")
    
    st.markdown("---")
    tab1, tab2 = st.tabs(["PENDIENTES", "INFORMADOS"])
    with tab1:
        if subir:
            st.button(f"👤 {subir.name[:20]}...", disabled=False)
        else:
            st.write("Sin estudios cargados")

# --- COLUMNA CENTRAL: VISOR ---
with col_centro:
    st.markdown("<div class='visor-container'>", unsafe_allow_html=True)
    if subir:
        # Lógica de carga idéntica a la v7.1
        if subir.name.lower().endswith('.dcm'):
            ds = pydicom.dcmread(subir)
            img_array = ds.pixel_array.astype(float)
            img_base = np.uint8((np.maximum(img_array, 0) / img_array.max()) * 255.0)
        else:
            file_bytes = np.asarray(bytearray(subir.read()), dtype=np.uint8)
            img_base = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
        
        # Ajustes de Sidebar (Brillo/Contraste) que se aplicarán aquí
        # Nota: En web, los sliders están en la barra lateral por eficiencia
    else:
        # Pantalla vacía como en el inicio de la v7.1
        dummy_img = np.zeros((600, 800), dtype=np.uint8)
        st.image(dummy_img, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Navegación inferior
    c1, c2, c3 = st.columns([1, 2, 1])
    c1.button("❮❮")
    c2.markdown("<h4 style='text-align: center;'>1 / 1</h4>", unsafe_allow_html=True)
    c3.button("❯❯")

# --- COLUMNA DERECHA: HERRAMIENTAS ---
with col_der:
    st.markdown("<h3 style='text-align: center;'>EXPLORACIÓN</h3>", unsafe_allow_html=True)
    t1, t2 = st.columns(2)
    t1.button("🔍", help="Lupa")
    t2.button("📏", help="Regla")
    
    st.markdown("<h3 style='text-align: center;'>AJUSTES</h3>", unsafe_allow_html=True)
    st.write("☀️ Brillo")
    brillo = st.slider("B", -100, 100, 0, label_visibility="collapsed")
    st.write("◑ Contraste")
    contra = st.slider("C", 0.5, 3.0, 1.0, label_visibility="collapsed")
    
    # Aplicar ajustes a la imagen si existe
    if subir and 'img_base' in locals():
        img_proc = cv2.convertScaleAbs(img_base, alpha=contra, beta=brillo)
        img_final = cv2.bitwise_not(img_proc) # Negativo automático v7.1
        col_centro.image(img_final, use_container_width=True)

    st.write("##")
    if st.button("📝 INFORME", type="primary"):
        st.info("Redactando informe...")EstacionRadiologica(); app.mainloop()
