import cv2
import pytesseract

# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\luiz.santos\Desktop\Code\pytesseract\tesseract.exe'

def ocr(image_path):
    # Carregar a imagem usando o OpenCV
    image = cv2.imread(image_path)

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

# Caminho para a imagem de entrada
image_path = 'imgs/img03.jpg'

# Executar o OCR na imagem
extracted_text = ocr(image_path)

# Exibir o texto extraído
print(extracted_text)