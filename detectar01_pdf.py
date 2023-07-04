import cv2
import fitz
from PIL import Image
import numpy as np


def detect_text_regions(image):
    # Converter a imagem para escala de cinza
    gray = image.convert('L')

    # Aplicar a binarização adaptativa
    _, binary = cv2.threshold(np.array(gray), 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

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

def process_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text_regions = []
    for page in doc:
        pix = page.get_pixmap()
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        regions = detect_text_regions(image)
        text_regions.extend(regions)

    return text_regions

# Caminho para o arquivo PDF
pdf_path = 'imgs/pdf02.pdf'

# Processar o PDF e detectar as regiões de texto em cada página
text_regions = process_pdf(pdf_path)

# Carregar a primeira página do PDF para exibir as regiões de texto destacadas
doc = fitz.open(pdf_path)
page = doc.load_page(0)
pix = page.get_pixmap()
image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

# Converter a imagem para o formato OpenCV
image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

# Desenhar retângulos ao redor das regiões de texto na imagem original
for (x1, y1, x2, y2) in text_regions:
    cv2.rectangle(image_cv, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Exibir a imagem com as regiões de texto destacadas
cv2.imshow('Texto Detectado', image_cv)
cv2.waitKey(0)
cv2.destroyAllWindows()
