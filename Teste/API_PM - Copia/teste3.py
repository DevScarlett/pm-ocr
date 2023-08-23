import os
import PyPDF2
import pytesseract
from PIL import Image
import re
from flask import Flask, request, jsonify
from pdf2image import convert_from_path
import time

app = Flask(__name__)

# Configurar o caminho para o executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\wallace.santos\Desktop\Tesseract\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = pytesseract.pytesseract.tesseract_cmd + ' -l por'

# Função para ajustar a frase de busca para a expressão regular
def ajustar_frase(frase):
    # Remover caracteres especiais e espaços
    return re.sub(r'[^0-9a-zA-Z]+', '', frase).lower()

# Função para extrair texto de um PDF
def ocr_pdf(pdf_path, frase_desejada):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text_extraido = ''
        resultados_pdf = []
        for page_number, page in enumerate(pdf_reader.pages, start=1):
            page_text = page.extract_text()
            text_extraido += page_text
            if ajustar_frase(frase_desejada) in ajustar_frase(page_text):
                resultados_pdf.append({'pdf': nome_arquivo, 'pagina': page_number})

    return text_extraido

# Função para extrair texto de uma imagem
def ocr_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

# Caminho da pasta contendo os arquivos PDF
pasta_pdf = r'C:\Users\wallace.santos\Documents\API_PM - Copia\Arquivos_Teste'

# Tempo de início da execução do código
start_time = time.time()

# Lista para armazenar os textos extraídos
textos_extraidos = []
for nome_arquivo in os.listdir(pasta_pdf):
    arquivo_path = os.path.join(pasta_pdf, nome_arquivo)
    if nome_arquivo.lower().endswith('.pdf'):
        # Extrair texto do PDF
        texto_extraido = ocr_pdf(arquivo_path, '')
        textos_extraidos.append(texto_extraido)

# Rota para extrair textos
@app.route('/extrair_textos', methods=['GET'])
def extrair_textos():
    return jsonify(textos_extraidos)



# Rota para pesquisar Frase e, se necessário, extrair texto de imagem
@app.route('/pesquisar_e_extrair', methods=['POST'])
def pesquisar_e_extrair():
    data = request.get_json()

    if 'tipo' not in data or 'nome' not in data:
        return jsonify({'error': 'Os campos "tipo" e "nome" são obrigatórios.'}), 400

    tipo = data['tipo']
    frase_desejada = data['nome']
    frase_ajustada = ajustar_frase(frase_desejada)  # Definir a variável aqui

    resultados = []  # Lista para armazenar os resultados

    for nome_arquivo in os.listdir(pasta_pdf):
        arquivo_path = os.path.join(pasta_pdf, nome_arquivo)
        if nome_arquivo.lower().endswith('.pdf'):
            # Limpar a lista de resultados para cada novo PDF
            resultados_pdf = []

            # Extrair texto do PDF
            texto_pdf = ocr_pdf(arquivo_path, frase_ajustada)

            if resultados_pdf:
                resultados.extend(resultados_pdf)

    imagem_path = data.get('imagem_path')
    if imagem_path:
        texto_extraido_imagem = ocr_image(imagem_path)
        if frase_ajustada in ajustar_frase(texto_extraido_imagem):
            resultados.append({'pdf': 'Imagem', 'pagina': 'Imagem'})

    if not resultados:
        return jsonify({'message': 'Nenhum resultado encontrado para a frase especificada.'}), 404
    
    return jsonify(resultados)

def format_time(seconds):
    minutes = int(seconds // 60)
    seconds %= 60
    return f"{minutes} minutos e {seconds:.2f} segundos"

elapsed_time = time.time() - start_time
print(f"Tempo até o código ser iniciado: {format_time(elapsed_time)}")
    
if __name__ == '__main__':
    app.run(debug=True)
