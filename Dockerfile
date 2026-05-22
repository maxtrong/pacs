# Usar una imagen base con entorno gráfico web (noVNC) integrado
FROM jlesage/baseimage-gui:ubuntu-22.04-v4

# Definir el nombre de la ventana de tu sistema
ENV APP_NAME="SISTEMA RADIOLOGICO PROFESIONAL V7.5 - MAXTRONG"

# Instalar dependencias del sistema operativo para que corra Tkinter y OpenCV
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-tk \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Instalar tus librerías de Python
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Copiar tu código original y tu imagen de Splash al servidor
COPY app.py /app/app.py
COPY "maxtrong pacs.png" /app/maxtrong pacs.png

# Crear el script de arranque automático de tu software
RUN echo "#!/bin/sh" > /startapp.sh && \
    echo "exec python3 /app/app.py" >> /startapp.sh && \
    chmod +x /startapp.sh