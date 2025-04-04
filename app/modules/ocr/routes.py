import os
from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
import requests
import wikipedia

ocr_bp = Blueprint('ocr', __name__, template_folder='../../templates/ocr')

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@ocr_bp.route('/', methods=['GET', 'POST'])
def index():
    imagem_path = None
    texto_extraido = None
    explicacao = None
    traducao = None

    if request.method == 'POST':
        # PROCESSAR IMAGEM
        if 'imagem' in request.files and request.files['imagem'].filename != '':
            imagem = request.files['imagem']
            if imagem and allowed_file(imagem.filename):
                if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)

                filename = secure_filename(imagem.filename)
                imagem_path = os.path.join(UPLOAD_FOLDER, filename)
                imagem.save(imagem_path)

                texto_extraido = pytesseract.image_to_string(Image.open(imagem_path), lang='spa').strip()

                wikipedia.set_lang("es")
                try:
                    explicacao = wikipedia.summary(texto_extraido, sentences=2)
                except:
                    explicacao = "No se encontró una explicación para el término."

                traducao = traduzir_para_portugues(explicacao)

        # PROCESSAR TEXTO MANUAL
        elif 'termo' in request.form:
            termo = request.form['termo'].strip()
            if termo:
                wikipedia.set_lang("es")
                try:
                    explicacao = wikipedia.summary(termo, sentences=2)
                except:
                    explicacao = "No se encontró una explicación para el término."
                traducao = traduzir_para_portugues(explicacao)

    return render_template('ocr/index.html',
                           imagem=imagem_path,
                           texto=texto_extraido,
                           explicacao=explicacao,
                           traducao=traducao)

def traduzir_para_portugues(texto):
    try:
        resposta = requests.post(
            "https://libretranslate.de/translate",
            headers={"Content-Type": "application/json"},
            json={
                "q": texto,
                "source": "es",
                "target": "pt",
                "format": "text"
            }
        )
        if resposta.status_code == 200:
            return resposta.json().get("translatedText", "Tradução não encontrada")
        else:
            return "Erro ao traduzir"
    except:
        return "Tradução indisponível no momento"
