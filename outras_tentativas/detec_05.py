import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\luiz.santos\Desktop\Code\pytesseract\tesseract.exe'

def cascade_segmentation(image_path):
    # Carregar a imagem colorida
    image = cv2.imread(image_path)

    # Converter a imagem para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar a segmentação baseada em limiar adaptativo
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # Aplicar o algoritmo de watershed
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    sure_bg = cv2.dilate(binary, kernel, iterations=3)
    dist_transform = cv2.distanceTransform(binary, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, 0.1 * dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    _, markers = cv2.connectedComponents(sure_fg)
    markers += 1
    markers[unknown == 255] = 0

    markers = cv2.watershed(image, markers)
    image[markers == -1] = [0, 0, 255]

    # Ler o texto nas regiões segmentadas
    text_regions = []
    for label in np.unique(markers):
        if label == -1:
            continue
        mask = np.zeros(gray.shape, dtype=np.uint8)
        mask[markers == label] = 255
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            text_region = gray[y:y+h, x:x+w]
            text = pytesseract.image_to_string(text_region, lang='eng')
            text_regions.append((x, y, x+w, y+h, text))

    return image, text_regions

# Caminho para a imagem
image_path = 'imgs/img01.png'

# Segmentar a imagem usando a abordagem em cascata e ler o texto
result, text_regions = cascade_segmentation(image_path)

# Exibir a imagem segmentada
cv2.imshow('Segmented Image', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
