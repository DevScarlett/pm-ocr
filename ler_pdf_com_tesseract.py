import fitz
import pytesseract
from PIL import Image

# Configurar o caminho para o executável do Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\luiz.santos\Desktop\Code\pytesseract\tesseract.exe'

def ocr_from_pdf(pdf_path):
    # Abrir o arquivo PDF
    with fitz.open(pdf_path) as pdf:
        # Inicializar uma variável para armazenar o texto extraído
        extracted_text = ''

        # Iterar sobre cada página do PDF
        for page in pdf:
            # Renderizar a página como uma imagem em escala de cinza
            pix = page.get_pixmap(alpha=False)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # Converter a imagem para escala de cinza
            img_gray = img.convert("L")

            # Extrair o texto da imagem usando o Tesseract OCR
            page_text = pytesseract.image_to_string(img_gray)

            # Adicionar o texto extraído ao resultado final
            extracted_text += page_text

    # Retornar o texto extraído do PDF
    return extracted_text

# Caminho para o arquivo PDF
pdf_path = 'imgs/pdf04.pdf'

# Executar o OCR no arquivo PDF
extracted_text = ocr_from_pdf(pdf_path)

# Exibir o texto extraído
print(extracted_text)
