import cv2
import pytesseract
import PyPDF2

def ocr_pdf(pdf_path):
    # abrindo pdf
    with open(pdf_path, 'rb') as file:
        # criando objeto pdf reader
        pdf_reader = PyPDF2.PdfReader(file)

        #var pra guardar texto extraido
        text_extraido =''

        #iterar nas paginas do pdf
        for page_number in range(len(pdf_reader.pages)):
            # pegando o objeto da pagina atual
            page_object = pdf_reader.pages[page_number]

            # extraindo o texto da pagina
            page_text = page_object.extract_text()

            # alocando texto extraido pro resultado final
            text_extraido += page_text
   
    
    # retornando texto extraido final
    return text_extraido

#caminho do pdf
pdf_path = 'imgs/pdf05.pdf'

# executando função pra ler e extrai texto do pdf
text_extraido = ocr_pdf(pdf_path)
# exibindo texto extraido
print(text_extraido)

if '901.189.875 -34' in text_extraido:
    print('\nAchou!')
else:
    print('\nNão achou')













from flask import Flask, request, jsonify
import os
import PyPDF2

app = Flask(__name__)

def ocr_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text_extraido = ''
        for page_number in range(len(pdf_reader.pages)):
            page_object = pdf_reader.pages[page_number]
            page_text = page_object.extract_text()
            
            # Verificar se existem 9 dígitos de CPF seguidos de um hífen
            cpf_com_hifen = page_text.replace(" ", "").replace(".", "").replace("\n", "")
            for i in range(len(cpf_com_hifen) - 10):
                if cpf_com_hifen[i:i+9].isdigit() and cpf_com_hifen[i+9] == "-":
                    # Caso seja encontrado, unir o hífen aos dígitos do CPF
                    page_text = page_text.replace(cpf_com_hifen[i:i+10], cpf_com_hifen[i:i+9] + "-")

            text_extraido += page_text

    return text_extraido

def validar_cpf(cpf):
    cpf_numerico = ''.join(filter(str.isdigit, cpf))
    return len(cpf_numerico) == 11

@app.route('/extrair_texto', methods=['POST'])
def extrair_texto():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado.'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nome do arquivo vazio.'}), 400

    if file and file.filename.lower().endswith('.pdf'):
        try:
            texto_extraido = ocr_pdf(file)
            return jsonify({'texto': texto_extraido})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Arquivo inválido. Por favor, envie um arquivo PDF.'}), 400

@app.route('/validar_cpf', methods=['POST'])
def validar_cpf_endpoint():
    data = request.get_json()
    if 'cpf' not in data:
        return jsonify({'error': 'Campo "cpf" é obrigatório.'}), 400

    cpf = data['cpf']
    if validar_cpf(cpf):
        return jsonify({'valido': True})
    else:
        return jsonify({'valido': False})

if __name__ == '__main__':
    app.run(debug=True)
