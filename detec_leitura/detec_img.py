
# Detecção de regiões de texto em uma imagem usando técnicas de binarização adaptativa, operações morfológicas e detecção de contornos. 
# O código carrega a imagem, converte para escala de cinza e aplica binarização adaptativa para obter uma imagem binária invertida.
# Em seguida, são aplicadas operações morfológicas de dilatação e erosão para melhorar a segmentação dos caracteres.
# A função findContours é usada para encontrar os contornos na imagem binarizada.
# O código então itera sobre os contornos encontrados e verifica critérios de área, largura e altura para identificar as regiões que podem conter texto.
# Essas regiões são armazenadas na lista text_regions.
# Por fim, o código carrega novamente a imagem original, desenha retângulos ao redor das regiões de texto identificadas e exibe a imagem resultante.

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
image_path = 'imgs/img04.png'

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
