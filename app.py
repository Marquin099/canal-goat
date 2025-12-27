import subprocess
from flask import Flask, Response

app = Flask(__name__)

# SEU LINK ORIGINAL
REMOTE_URL = "http://208.115.239.254:14784"

@app.route('/')
def home():
    return "Servidor IPTV Ativo! Use o caminho /canal.ts no seu player."

@app.route('/canal.ts')
def stream():
    # O FFmpeg vai ler o link e entregar um fluxo limpo (mpegts) para a TV
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', REMOTE_URL,
        '-c', 'copy',      # Copia o vídeo sem processar (economiza CPU do Koyeb)
        '-f', 'mpegts',    # Formato que as Smart TVs aceitam bem via HTTP
        'pipe:1'           # Envia para a saída do script
    ]
    
    process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def generate():
        try:
            while True:
                chunk = process.stdout.read(1024 * 64) # Blocos de 64KB
                if not chunk:
                    break
                yield chunk
        finally:
            process.kill() # Garante que o processo feche se você parar de assistir

    return Response(generate(), mimetype='video/mp2t')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
