import os
import PyPDF2
import pytesseract
from PIL import Image
import re
from flask import Flask, request, jsonify
from pdf2image import convert_from_path
import time
from validate_docbr import CPF 
from nameparser import HumanName
#Para instalar todas as dependências do código utilize pip install -r requirements.txt
app = Flask(__name__)

# Configurar o caminho para o executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\wallace.santos\Desktop\Tesseract\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = pytesseract.pytesseract.tesseract_cmd + ' -l por'

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
pasta_pdf = r'C:\Users\wallace.santos\Documents\API_PM - Copia\Arquivos_Teste'

# Tempo de início da execução do código
start_time = time.time()

# Lista para armazenar os textos extraídos
textos_extraidos = []
for nome_arquivo in os.listdir(pasta_pdf):
    arquivo_path = os.path.join(pasta_pdf, nome_arquivo)
    if nome_arquivo.lower().endswith('.pdf'):
        # Extrair texto do PDF
        texto_extraido = ocr_pdf(arquivo_path)
        textos_extraidos.append(texto_extraido)

# Rota para extrair textos
@app.route('/extrair_textos', methods=['GET'])
def extrair_textos():
    return jsonify(textos_extraidos)

# Função para ajustar a frase de busca para a expressão regular
def ajustar_frase(frase):
    # Remover caracteres especiais e espaços
    return re.sub(r'[^0-9a-zA-Z]+', '', frase).lower()
def validar_cpf(cpf):
    cpf_validator = CPF()
    return cpf_validator.validate(cpf)
def validar_nome(nome_completo):
    name = HumanName(nome_completo)
    
    # Verificar se existem componentes do nome
    if not name.first or not name.last:
        return False
    
    return True

# Rota para pesquisar Frase e, se necessário, extrair texto de imagem
@app.route('/pesquisar', methods=['POST'])
def pesquisar():
    data = request.get_json()

    if 'tipo' not in data or 'busca' not in data:
        return jsonify({'error': 'Os campos "tipo" e "busca" são obrigatórios.'}), 400

    tipo = data['tipo']
    frase_desejada = data['busca']

    resultados_texto = []
    resultados_imagem = []
    frase_ajustada = ajustar_frase(frase_desejada)

    for idx, texto in enumerate(textos_extraidos):
        texto_ajustado = ajustar_frase(texto)
        if tipo == 'buscar' and frase_ajustada in texto_ajustado:
            resultados_texto.append(os.listdir(pasta_pdf)[idx])

    imagem_path = data.get('imagem_path')
    if imagem_path:
        texto_extraido_imagem = ocr_image(imagem_path)
        if frase_ajustada in ajustar_frase(texto_extraido_imagem):
            resultados_imagem.append('Imagem')

    if resultados_texto:
        return jsonify(resultados_texto)
    else:
        if imagem_path:
            images = convert_from_path(imagem_path)
            for i, image in enumerate(images):
                image.save(f'image_{i}.jpg')  # Salva a imagem como arquivo para posterior processamento
                texto_extraido_imagem = ocr_image(f'image_{i}.jpg')
                if frase_ajustada in ajustar_frase(texto_extraido_imagem):
                    resultados_imagem.append('Imagem')
                    break  # Para após encontrar em uma das imagens

    if resultados_imagem:
        return jsonify(resultados_imagem)
    else:
        return jsonify({'message': 'Nenhum resultado encontrado para a frase especificada.'}), 404

@app.route('/cpf', methods=['POST'])
def cpf():
    data = request.get_json()

    if 'tipo' not in data or 'cpf' not in data:
        return jsonify({'error': 'Os campos "tipo" e "cpf" são obrigatórios.'}), 400

    tipo = data['tipo']
    cpf_desejado = data['cpf']

    if not validar_cpf(cpf_desejado):
        return jsonify({'error': 'CPF inválido.'}), 400

    resultados_texto = []
    resultados_imagem = []
    frase_ajustada = ajustar_frase(cpf_desejado)

    for idx, texto in enumerate(textos_extraidos):
        texto_ajustado = ajustar_frase(texto)
        if tipo == 'buscar' and frase_ajustada in texto_ajustado:
            resultados_texto.append(os.listdir(pasta_pdf)[idx])

    imagem_path = data.get('imagem_path')
    if imagem_path:
        texto_extraido_imagem = ocr_image(imagem_path)
        if frase_ajustada in ajustar_frase(texto_extraido_imagem):
            resultados_imagem.append('Imagem')

    if resultados_texto:
        return jsonify(resultados_texto)
    else:
        if imagem_path:
            images = convert_from_path(imagem_path)
            for i, image in enumerate(images):
                image.save(f'image_{i}.jpg')  # Salva a imagem como arquivo para posterior processamento
                texto_extraido_imagem = ocr_image(f'image_{i}.jpg')
                if frase_ajustada in ajustar_frase(texto_extraido_imagem):
                    resultados_imagem.append('Imagem')
                    break  # Para após encontrar em uma das imagens

@app.route('/nome', methods=['POST'])
def nome():
    data = request.get_json()

    if 'tipo' not in data or 'nome' not in data:
        return jsonify({'error': 'Os campos "tipo" e "nome" são obrigatórios.'}), 400

    tipo = data['tipo']
    nome_desejado = data['nome']

    if not validar_nome(nome_desejado):
        return jsonify({'error': 'Nome inválido ou incompleto.'}), 400

    resultados_texto = []
    resultados_imagem = []

    for idx, texto in enumerate(textos_extraidos):
        resultados_texto.append(os.listdir(pasta_pdf)[idx])

    imagem_path = data.get('imagem_path')
    if imagem_path:
        texto_extraido_imagem = ocr_image(imagem_path)
        resultados_imagem.append('Imagem')

    if resultados_texto:
        return jsonify(resultados_texto)
    else:
        if imagem_path:
            images = convert_from_path(imagem_path)
            for i, image in enumerate(images):
                image.save(f'image_{i}.jpg')  # Salva a imagem como arquivo para posterior processamento
                texto_extraido_imagem = ocr_image(f'image_{i}.jpg')
                resultados_imagem.append('Imagem')
                break  # Para após encontrar em uma das imagens

    if resultados_imagem:
        return jsonify(resultados_imagem)
    else:
        return jsonify({'message': 'Nenhum resultado encontrado para o nome especificado.'}), 404

def format_time(seconds):
    minutes = int(seconds // 60)
    seconds %= 60
    return f"{minutes} minutos e {seconds:.2f} segundos"

elapsed_time = time.time() - start_time
print(f"Tempo até o código ser iniciado: {format_time(elapsed_time)}")
    
if __name__ == '__main__':
    app.run(debug=True)

