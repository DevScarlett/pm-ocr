import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\luiz.santos\Desktop\Code\pytesseract\tesseract.exe'

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

def perform_ocr(image, regions):
    ocr_results = []
    for (x1, y1, x2, y2) in regions:
        # Recortar a região de texto da imagem original
        region_of_interest = image[y1:y2, x1:x2]

        # Converter a região de interesse para escala de cinza
        gray = cv2.cvtColor(region_of_interest, cv2.COLOR_BGR2GRAY)

        custom_config = r'--oem 3 --psm 1 -l por'
        # Realizar OCR na região de interesse usando o Tesseract
        text = pytesseract.image_to_string(gray, config=custom_config)

        # Adicionar o resultado do OCR à lista de resultados
        ocr_results.append({'text': text, 'coordinates': (x1, y1, x2, y2), 'image': region_of_interest})

    return ocr_results

# Caminho para a imagem
image_path = 'imgs/img03.jpg'

# Detectar as regiões de texto na imagem
text_regions = detect_text_regions(image_path)

# Carregar a imagem original
image = cv2.imread(image_path)

# Realizar OCR nas regiões de texto identificadas
ocr_results = perform_ocr(image, text_regions)

# Exibir os resultados
for result in ocr_results:
    print('Texto:', result['text'])
    #print('Coordenadas:', result['coordinates'])
    print('---')
