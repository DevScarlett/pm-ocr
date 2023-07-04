import cv2
import pytesseract
import easyocr
from PIL import Image
import numpy as np

def detect_text_regions(image):
    reader = easyocr.Reader(['en'])
    bounds = reader.readtext(image, detail=0, paragraph=True)
    
    text_regions = []
    for bound in bounds:
        x1, y1, x2, y2 = bound[0][0], bound[0][1], bound[2][0], bound[2][1]
        text_regions.append((x1, y1, x2, y2))
    
    return text_regions

def process_image(image_path):
    image = Image.open(image_path).convert('RGB')
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

    # Redimensionar a imagem
    ratio = 800 / gray.shape[1]  # Defina a largura desejada aqui (800 no exemplo)
    img = cv2.resize(gray, (int(gray.shape[1] * ratio), 800), interpolation=cv2.INTER_LINEAR)
    img = Image.fromarray(img)

    # Detectar as regiões de texto na imagem
    text_regions = detect_text_regions(img)

    # Realizar OCR apenas nas regiões de texto
    extracted_text = []
    for (x1, y1, x2, y2) in text_regions:
        region_image = img.crop((x1, y1, x2, y2))
        text = pytesseract.image_to_string(region_image, lang='eng')
        extracted_text.append({'text': text, 'region': (x1, y1, x2, y2)})

    return extracted_text

# Caminho para a imagem
image_path = 'imgs\img01.png'

# Processar a imagem e realizar OCR nas regiões de textos
extracted_text = process_image(image_path)

# Exibir os resultados
for result in extracted_text:
    print('Texto:', result['text'])
    print('Região:', result['region'])
    print('---')
