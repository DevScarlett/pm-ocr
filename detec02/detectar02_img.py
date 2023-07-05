import cv2
import numpy as np

# Carregar a imagem
image = cv2.imread('imgs/img03.jpg', cv2.IMREAD_GRAYSCALE)

# Aplicar uma limiarização para obter uma imagem binária
_, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Realizar a rotulagem dos componentes conectados
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_image, connectivity=8)

# Descartar o primeiro componente conectado, pois é o plano de fundo
stats = stats[1:]
centroids = centroids[1:]

# Iterar sobre os componentes conectados
for i, stat in enumerate(stats):
    # Extrair informações do componente conectado
    x, y, width, height, area = stat

    # Desenhar um retângulo ao redor da região de texto
    cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)

# Exibir a imagem com as regiões de texto destacadas
cv2.imshow('Segmented Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
