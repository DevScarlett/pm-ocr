import os
import PyPDF2
import pytesseract
from PIL import Image
import io
import fitz
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configurar o caminho para o executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Users/decio.faria/Projetos/VScode/API_PM/OCR/tesseract.exe'

# Função para extrair texto de um PDF
def ocr_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text_extraido = ''
        for page_number in range(len(pdf_reader.pages)):
            page_object = pdf_reader.pages[page_number]
            page_text = page_object.extract_text()
            text_extraido += page_text

    return text_extraido

# Função para extrair texto de uma imagem
def ocr_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

# Caminho da pasta contendo os arquivos PDF
pasta_pdf = r'C:/Users/decio.faria/Projetos/VScode/API_PM/Arquivos_Teste'

# Lista para armazenar os textos extraídos
textos_extraidos = []
for nome_arquivo in os.listdir(pasta_pdf):
    arquivo_path = os.path.join(pasta_pdf, nome_arquivo)
    if nome_arquivo.lower().endswith('.pdf'):
        # Extrair texto do PDF
        texto_extraido = ocr_pdf(arquivo_path)
        textos_extraidos.append(texto_extraido)

        # Abrir o PDF com fitz para extrair texto de imagens
        doc = fitz.open(arquivo_path)
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            images = page.get_images(full=True)
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image = Image.open(io.BytesIO(base_image["image"]))
                texto_imagem = pytesseract.image_to_string(image)
                textos_extraidos[-1] += texto_imagem

# Rota para extrair textos
@app.route('/extrair_textos', methods=['GET'])
def extrair_textos():
    return jsonify(textos_extraidos)

# Rota para pesquisar CPF
@app.route('/pesquisar', methods=['POST'])
def pesquisar():
    data = request.get_json()

    if 'tipo' not in data or 'termo' not in data:
        return jsonify({'error': 'Os campos "tipo" e "termo" são obrigatórios.'}), 400

    tipo = data['tipo']
    termo = data['termo']

    resultados = []
    for idx, texto in enumerate(textos_extraidos):
        if tipo == 'buscar':
                buscar = termo
                buscar_parte = buscar.replace(".", "").replace("-", "")[:5]
                if buscar_parte in texto.replace(".", "").replace("-", ""):
                    resultados.append(os.listdir(pasta_pdf)[idx])
                elif buscar_parte not in texto:
                    print("Não foi encontrado nenhum resultado para essa pesquisa")

    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True)
