import cv2
import pytesseract
import fitz
from PIL import Image
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\luiz.santos\Desktop\Code\pytesseract\tesseract.exe'

def detect_text_regions(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilate = cv2.dilate(binary, kernel, iterations=3)
    erode = cv2.erode(dilate, kernel, iterations=2)

    contours, _ = cv2.findContours(erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    text_regions = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)
        if area > 100 and w > 10 and h > 10:
            text_regions.append((x, y, x + w, y + h))

    return text_regions

def process_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text_results = []

    for page in doc:
        pix = page.get_pixmap()
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        text_regions = detect_text_regions(cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR))

        for (x1, y1, x2, y2) in text_regions:
            region_image = image.crop((x1, y1, x2, y2))
            text = pytesseract.image_to_string(region_image, lang='eng')
            text_results.append({'page': page.number + 1, 'text': text, 'region': (x1, y1, x2, y2)})

    doc.close()
    return text_results

# Caminho para o arquivo PDF
pdf_path = 'imgs/pdf02.pdf'

# Processar o PDF e realizar OCR em cada região de texto
extracted_text = process_pdf(pdf_path)

# Exibir os resultados
for result in extracted_text:
    #print('Página:', result['page'])
    #print('Texto:', result['text'])
    print(result['text'])
    #print('Região:', result['region'])
    #print('---')
