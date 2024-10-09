# Usar la imagen base de Firefox
FROM linuxserver/firefox:latest

# Instalar Python y xvfb
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Crear un entorno virtual de Python
RUN python3 -m venv /venv

# Instalar FastAPI y Selenium en el entorno virtual
RUN /venv/bin/pip install --no-cache-dir fastapi uvicorn selenium

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar tu aplicación FastAPI al contenedor
COPY ./app /app

# Exponer puertos para Firefox
EXPOSE 3000
EXPOSE 3001
# Exponer el puerto para FastAPI
EXPOSE 4321

# Comando por defecto para ejecutar FastAPI con xvfb
CMD ["bash", "-c", "xvfb-run -a /venv/bin/uvicorn main:app --host 0.0.0.0 --port 4321 --reload"]
