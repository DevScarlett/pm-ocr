import cv2
import pytesseract
import PyPDF2

def ocr(image):
    # Converter a imagem para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar um pré-processamento na imagem (opcional)
    # Aqui você pode fazer operações como redimensionamento, remoção de ruído, etc.

    # Configurar o idioma como português
    custom_config = r'--oem 3 --psm 1 -l por'

    # Usar o Tesseract para realizar OCR na imagem
    text = pytesseract.image_to_string(gray, config=custom_config)

    # Retornar o texto extraído
    return text

def process_pdf(pdf_path):
    # Abrir o arquivo PDF
    with open(pdf_path, 'rb') as file:
        # Criar um objeto PDFReader
        pdf_reader = PyPDF2.PdfReader(file)

        # Inicializar uma variável para armazenar o texto extraído
        extracted_text = ''

        # Iterar sobre cada página do PDF
        for page_number in range(len(pdf_reader.pages)):
            # Obter o objeto Page atual
            page_object = pdf_reader.pages[page_number]

            # Extrair o texto da página usando o método extract_text()
            page_text = page_object.extract_text()

            # Adicionar o texto extraído ao resultado final
            extracted_text += page_text

    # Retornar o texto extraído do PDF
    return extracted_text

# Caminho para o arquivo PDF
pdf_path = 'imgs/pdf02.pdf'

# Executar o OCR no arquivo PDF
extracted_text = process_pdf(pdf_path)

# Exibir o texto extraído
print(extracted_text)
