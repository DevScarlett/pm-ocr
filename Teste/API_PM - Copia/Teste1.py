import os
import PyPDF2
import pytesseract
from PIL import Image
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuração do Tesseract
TESSERACT_CMD = r'C:/Users/decio.faria/Projetos/VScode/API_PM/OCR/tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

# Função para extrair texto de um PDF
def ocr_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text_extraido = ''
        for page_object in pdf_reader.pages:
            page_text = page_object.extract_text()
            text_extraido += page_text
    return text_extraido

# Caminho da pasta contendo os arquivos PDF
PASTA_PDF = r'C:/Users/decio.faria/Projetos/VScode/API_PM/Arquivos_Teste'

# Lista para armazenar os textos extraídos
textos_extraidos = [ocr_pdf(os.path.join(PASTA_PDF, nome_arquivo)) for nome_arquivo in os.listdir(PASTA_PDF) if nome_arquivo.lower().endswith('.pdf')]

# Rota para pesquisar termos
@app.route('/pesquisar', methods=['POST'])
def pesquisar_termos():
    data = request.get_json()

    if 'tipo' not in data or 'termos' not in data:
        return jsonify({'error': 'Os campos "tipo" e "termos" são obrigatórios.'}), 400
    
    tipo = data['tipo']
    termos_desejados = data['termos']

    resultados = []

    for idx, texto in enumerate(textos_extraidos):
        if tipo == 'buscar':
            buscar = termos_desejados.replace(".", "").replace("-", "")
            texto_limpo = texto.replace(".", "").replace("-", "")
        
        if buscar in texto_limpo:
            resultados.append(os.listdir(PASTA_PDF)[idx])
        else:
            print("Não foi encontrado nenhum resultado para essa pesquisa")

    if not resultados:
        return jsonify({'message': 'Nenhum resultado encontrado para os termos especificados.'}), 404

    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True)

