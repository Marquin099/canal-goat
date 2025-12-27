FROM python:3.9-slim

# Instala o FFmpeg no sistema do servidor
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

# Comando para rodar o servidor
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app", "--timeout", "0"]
