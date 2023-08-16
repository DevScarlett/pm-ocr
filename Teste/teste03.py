import os
import PyPDF2
import pytesseract
from PIL import Image
import io
import fitz
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configurar o caminho para o executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\wallace.santos\\Desktop\\Tesseract\\tesseract.exe'

def ocr_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text_extraido = ''
        for page_number in range(len(pdf_reader.pages)):
            page_object = pdf_reader.pages[page_number]
            page_text = page_object.extract_text()

            cpf_com_hifen = page_text.replace(" ", "").replace(".", "").replace("\n", "")
            for i in range(len(cpf_com_hifen) - 10):
                if cpf_com_hifen[i:i+9].isdigit() and cpf_com_hifen[i+9] == "-":
                    page_text = page_text.replace(cpf_com_hifen[i:i+10], cpf_com_hifen[i:i+9] + "-")

            text_extraido += page_text

    return text_extraido

def ocr_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def validar_cpf(cpf):
    cpf_numerico = ''.join(filter(str.isdigit, cpf))
    if len(cpf_numerico) != 11:
        return False

    if cpf_numerico == cpf_numerico[0] * 11:
        return False

    total = 0
    for i in range(9):
        total += int(cpf_numerico[i]) * (10 - i)
    resto = total % 11
    digito1 = 0 if resto < 2 else 11 - resto

    total = 0
    for i in range(10):
        total += int(cpf_numerico[i]) * (11 - i)
    resto = total % 11
    digito2 = 0 if resto < 2 else 11 - resto

    if int(cpf_numerico[9]) == digito1 and int(cpf_numerico[10]) == digito2:
        return True
    else:
        return False

def validar_rg(rg):
    rg_numerico = ''.join(filter(str.isdigit, rg))
    return len(rg_numerico) == 9

pasta_pdf = r'C:\Users\wallace.santos\Documents\GitHub\pm-ocr\Teste\imgs'

textos_extraidos = []
for nome_arquivo in os.listdir(pasta_pdf):
    arquivo_path = os.path.join(pasta_pdf, nome_arquivo)
    if nome_arquivo.lower().endswith('.pdf'):
        texto_extraido = ocr_pdf(arquivo_path)
        textos_extraidos.append(texto_extraido)

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

@app.route('/extrair_textos', methods=['GET'])
def extrair_textos():
    return jsonify(textos_extraidos)

@app.route('/pesquisar', methods=['POST'])
def pesquisar():
    data = request.get_json()

    if 'tipo' not in data or 'termo' not in data:
        return jsonify({'error': 'Os campos "tipo" e "termo" são obrigatórios.'}), 400

    tipo = data['tipo']
    termo = data['termo']

    resultados = []
    for idx, texto in enumerate(textos_extraidos):
        if tipo == 'termos' and termo in texto:
            resultados.append(os.listdir(pasta_pdf)[idx])
        elif tipo == 'cpf':
            if validar_cpf(termo):
                cpf_parte = termo.replace(".", "").replace("-", "")[:5]
                if cpf_parte in texto.replace(".", "").replace("-", ""):
                    resultados.append(os.listdir(pasta_pdf)[idx])
        elif tipo == 'rg':
            if validar_rg(termo):
                rg_parte = termo.replace(".", "").replace("-", "")[:5]
                if rg_parte in texto.replace(".", "").replace("-", ""):
                    resultados.append(os.listdir(pasta_pdf)[idx])

    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True)
