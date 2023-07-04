
# métodos de binarização e segmentação

import cv2

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

# Caminho para a imagem
image_path = 'imgs/img03.jpg'

# Detectar as regiões de texto na imagem
text_regions = detect_text_regions(image_path)

# Desenhar retângulos ao redor das regiões de texto na imagem original
image = cv2.imread(image_path)
for (x1, y1, x2, y2) in text_regions:
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Exibir a imagem com as regiões de texto destacadas
cv2.imshow('Texto Detectado', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
