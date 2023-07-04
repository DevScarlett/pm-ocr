import cv2
import pytesseract
import easyocr

def detect_text_regions(image):
    reader = easyocr.Reader(['en'])
    bounds = reader.readtext(image, detail=0, paragraph=True)
    
    text_regions = []
    for bound in bounds:
        x1, y1, x2, y2 = bound[0][0], bound[0][1], bound[2][0], bound[2][1]
        text_regions.append((x1, y1, x2, y2))
    
    return text_regions

def process_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detectar as regiões de texto na imagem
    text_regions = detect_text_regions(gray)

    # Realizar OCR apenas nas regiões de texto
    extracted_text = []
    for (x1, y1, x2, y2) in text_regions:
        region_image = gray[y1:y2, x1:x2]
        text = pytesseract.image_to_string(region_image, lang='eng')
        extracted_text.append({'text': text, 'region': (x1, y1, x2, y2)})

    return extracted_text

# Caminho para a imagem
image_path = 'imgs/img03.jpg'

# Processar a imagem e realizar OCR nas regiões de texto
extracted_text = process_image(image_path)

# Exibir os resultados
for result in extracted_text:
    print('Texto:', result['text'])
    print('Região:', result['region'])
    print('---')
