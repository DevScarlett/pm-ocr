import cv2
import pytesseract

#caminho do executável do tesseract (erro no path windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\luiz.santos\Desktop\Code\pytesseract\tesseract.exe'

def ocr(image_path):
    # carregando imagem
    image = cv2.imread(image_path)

    # convertendo imagem para escala de cinza
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar pré-processamento na imagem
    # Fazer operações como redimensionamento, remoção de ruído, etc.
    
    # configuração para o tesseract
    custom_config = r'--oem 3 --psm 1 -l por'

    # ocr na imagem usando o tesseract e a configuração anterior
    text = pytesseract.image_to_string(image_gray, config=custom_config)

    # retornando texto extraido no OCR acima
    return text

# caminho da imagem
image_path = 'imgs/img04.png'

# chamando função ocr
text_extraido = ocr(image_path)

# exibindo o texto extraido
print(text_extraido)