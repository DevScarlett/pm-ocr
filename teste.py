import cv2
import pytesseract

# Configurar o caminho para o executável do Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\luiz.santos\Desktop\Code\pytesseract\tesseract.exe'

def ocr(image_path):
    # Carregar a imagem usando o OpenCV
    image = cv2.imread(image_path)

    # Converter a imagem para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar a remoção de ruído
    denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)

    # Aplicar um pré-processamento adicional, se necessário
    # Aqui você pode adicionar mais etapas de pré-processamento, como binarização, redimensionamento, etc.

    # Configurar o idioma como português
    custom_config = r'--oem 3 --psm 6 -l por'

    # Usar o Tesseract para realizar OCR na imagem denoised
    text = pytesseract.image_to_string(denoised, config=custom_config)

    # Retornar o texto extraído
    return text

# Caminho para a imagem de entrada
image_path = 'imgs/img03.jpg'

# Executar o OCR na imagem com remoção de ruído
extracted_text = ocr(image_path)

# Exibir o texto extraído
print(extracted_text)
