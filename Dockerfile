FROM python:3.9-slim

# Instala o FFmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Define a pasta de trabalho
WORKDIR /app

# Copia os arquivos do GitHub para dentro do servidor
COPY . /app

# Instala as bibliotecas Python
RUN pip install --no-cache-dir flask gunicorn

# Comando para iniciar o servidor na porta 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app", "--timeout", "0"]
