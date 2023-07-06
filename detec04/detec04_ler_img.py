import cv2
import numpy as np
import pytesseract



def detect_text_regions(image_path):
    # Carregar a imagem
    image = cv2.imread(image_path)

    # Converter a imagem para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar a binarização adaptativa
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # Aplicar operações morfológicas para melhorar a segmentação
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilate = cv2.dilate(binary, kernel, iterations=3)
    erode = cv2.erode(dilate, kernel, iterations=2)

    # Encontrar os contornos na imagem binarizada
    contours, _ = cv2.findContours(erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Detectar regiões retangulares que podem conter texto
    text_regions = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)
        if area > 100 and w > 10 and h > 10:
            text_regions.append((x, y, x + w, y + h))

    return text_regions

def read_text(image, region):
    x1, y1, x2, y2 = region

    # Recortar a região de texto da imagem original
    roi = image[y1:y2, x1:x2]

    # Converter a região de texto para escala de cinza
    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Realizar a leitura de texto na região
    custom_config = r'--oem 3 --psm 0'
    text = pytesseract.image_to_string(roi_gray, config=custom_config)
    # text = pytesseract.image_to_string(roi_gray)

    return text

# Caminho para a imagem
image_path = 'imgs/img02.webp'

# Detectar as regiões de texto na imagem
text_regions = detect_text_regions(image_path)

# Carregar a imagem original
image = cv2.imread(image_path)

# Configurar o Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\luiz.santos\Desktop\Code\pytesseract\tesseract.exe'  # Caminho para o executável do Tesseract OCR

# Iterar sobre as regiões de texto e realizar a leitura
for region in text_regions:
    # Ler o texto na região
    text = read_text(image, region)

    # Imprimir o texto encontrado
    print(text)

    # Desenhar um retângulo ao redor da região de texto na imagem original
    x1, y1, x2, y2 = region
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Exibir a imagem com as regiões de texto destacadas
cv2.imshow('Texto Detectado', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
