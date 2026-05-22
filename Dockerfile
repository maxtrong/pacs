# Usamos una base que ya tiene Python 3 y entorno gráfico preinstalado y configurado
FROM banyb/python-tkinter-vnc:latest

# Nombre de la ventana
ENV APP_NAME="SISTEMA RADIOLOGICO PROFESIONAL V7.5 - MAXTRONG"

# Cambiar al directorio de trabajo correcto
WORKDIR /app

# Copiar tus archivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY maxtrong_pacs.png .

# Exponer el puerto del entorno gráfico web
EXPOSE 8080

# Comando directo de arranque
CMD ["python", "app.py"]
