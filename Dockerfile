FROM python:3.9-slim

# Instalar ffmpeg
RUN apt-get update && apt-get install -y ffmpeg
# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de requerimientos para instalar dependencias
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Asegurarse de que uvicorn esté instalado (opcional si ya está en requirements.txt)
RUN pip install uvicorn



# Copiar el código de la aplicación
COPY . /app

# Comando para iniciar la aplicación con uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
