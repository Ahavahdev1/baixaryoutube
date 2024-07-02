from flask import Flask, render_template_string, request, send_file
from pytube import YouTube
import os
import re

app = Flask(__name__)

# Caminho onde os vídeos serão salvos
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# HTML template como string
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Baixar Vídeos do YouTube</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            flex-direction: column;
        }

        .container {
            text-align: center;
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
        }

        input[type="text"] {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 4px;
        }

        button {
            padding: 10px 20px;
            border: none;
            background-color: #007BFF;
            color: white;
            border-radius: 4px;
            cursor: pointer;
        }

        button:hover {
            background-color: #0056b3;
        }

        .image-container img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
            padding-top: 20px;
        }
    </style>
</head>
<body>
    <!-- Espaço para a imagem -->
    <div class="image-container">
        <img src="/imagem.png" alt="Topo do Site">
    </div>
    <div class="container">
        <h2 class="text-center">Baixar Vídeos do YouTube</h2>
        <form action="/download" method="POST">
            <div class="form-group">
                <label for="url">URL do Vídeo do YouTube:</label>
                <input type="text" class="form-control" id="url" name="url" placeholder="Insira a URL do vídeo" required>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Baixar</button>
        </form>
    </div>

    <!-- Scripts -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']
    try:
        # Criar objeto YouTube e selecionar a melhor qualidade de vídeo disponível
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()

        # Nome do arquivo original do vídeo
        original_title = yt.title
        
        # Substituir caracteres inválidos para nomes de arquivos no Windows
        safe_title = re.sub(r'[\\/*?:"<>|]', "_", original_title)
        file_path = os.path.join(DOWNLOAD_FOLDER, f"{safe_title}.mp4")

        # Baixar o vídeo
        stream.download(output_path=DOWNLOAD_FOLDER, filename=f"{safe_title}.mp4")

        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return f"Erro ao baixar o vídeo: {e}", 500

# Rota para servir arquivos estáticos, como imagens
@app.route('/<path:filename>')
def static_files(filename):
    return send_file(filename)

if __name__ == "__main__":
    app.run(debug=True)
