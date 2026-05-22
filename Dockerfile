FROM jlesage/baseimage-gui:ubuntu-22.04-v4

ENV APP_NAME="SISTEMA RADIOLOGICO PROFESIONAL V7.5 - MAXTRONG"

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-tk \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Rutas limpias sin espacios
COPY app.py /app/app.py
COPY maxtrong_pacs.png /app/maxtrong_pacs.png

RUN echo "#!/bin/sh" > /startapp.sh && \
    echo "exec python3 /app/app.py" >> /startapp.sh && \
    chmod +x /startapp.sh
