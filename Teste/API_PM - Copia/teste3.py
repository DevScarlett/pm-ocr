import os
import pytesseract
import re
import io
import fitz  # PyMuPDF
from PIL import Image  # Certifique-se de que esta importação está presente no início do código
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configurar o caminho para o executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\wallace.santos\Desktop\Tesseract\tesseract.exe'

# Função para extrair texto de um PDF
def ocr_pdf(pdf_path):
    text_extraido = ''
    pdf_document = fitz.open(pdf_path)
    
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        page_text = page.get_text()
        text_extraido += page_text
    
    pdf_document.close()
    return text_extraido

def extrair_imagens(pdf_path):
    imagens = []
    pdf_document = fitz.open(pdf_path)
    
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_data = base_image["image"]
            pil_image = Image.open(io.BytesIO(image_data))  # Corrigido o uso do PIL
            imagens.append(pil_image)
    
    pdf_document.close()
    return imagens


# Função para extrair texto de uma imagem
def ocr_image(image_path):
    image = image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

# Caminho da pasta contendo os arquivos PDF
pasta_pdf = r'C:\Users\wallace.santos\Documents\API_PM - Copia\Arquivos_Teste'

# Lista para armazenar os textos extraídos
textos_extraidos = []
for nome_arquivo in os.listdir(pasta_pdf):
    arquivo_path = os.path.join(pasta_pdf, nome_arquivo)
    if nome_arquivo.lower().endswith('.pdf'):
        # Extrair texto do PDF
        texto_extraido = ocr_pdf(arquivo_path)
        textos_extraidos.append(texto_extraido)

        # Extrair imagens do PDF e processá-las
        imagens = extrair_imagens(arquivo_path)
        for pil_image in imagens:
            img_text = pytesseract.image_to_string(pil_image)
            textos_extraidos.append(img_text)

# Rota para extrair textos de PDFs
@app.route('/extrair_textos', methods=['GET'])
def extrair_textos():
    return jsonify(textos_extraidos)

# Função para ajustar a frase de busca para a expressão regular
def ajustar_frase(frase):
    # Remover caracteres especiais e espaços
    return re.sub(r'[^0-9a-zA-Z]+', '', frase).lower()

# Rota para pesquisar Frase
@app.route('/pesquisar', methods=['POST'])
def pesquisar_frase():
    data = request.get_json()

    if 'tipo' not in data or 'frase' not in data:
        return jsonify({'error': 'Os campos "tipo" e "frase" são obrigatórios.'}), 400
    
    tipo = data['tipo']
    frase_desejada = data['frase']
    
    resultados = []
    frase_ajustada = ajustar_frase(frase_desejada)
    
    for idx, texto in enumerate(textos_extraidos):
        texto_ajustado = ajustar_frase(texto)
        if tipo == 'buscar' and frase_ajustada in texto_ajustado:
            resultados.append(os.listdir(pasta_pdf)[idx])
    
    if not resultados:
        return jsonify({'message': 'Nenhum resultado encontrado para a frase especificada.'}), 404
    
    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True)
