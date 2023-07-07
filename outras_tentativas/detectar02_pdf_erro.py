import cv2
import numpy as np
import fitz
import tempfile
import os
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\luiz.santos\Desktop\Code\pytesseract\tesseract.exe'

def segment_pdf(pdf_path):
    # Abrir o arquivo PDF com o PyMuPDF
    doc = fitz.open(pdf_path)

    # Criar um diretório temporário para armazenar as imagens
    temp_dir = tempfile.mkdtemp()

    # Configurar o Tesseract OCR
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\luiz.santos\Desktop\Code\pytesseract\tesseract.exe'

    # Iterar sobre as páginas do PDF
    for page_num in range(len(doc)):
        # Obter a página atual
        page = doc.load_page(page_num)

        # Renderizar a página como uma imagem
        pix = page.get_pixmap()

        # Converter a imagem em um array numpy
        image_np = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)

        # Converter a imagem para o tipo uint8
        image_np = image_np.astype(np.uint8)

        # Salvar a imagem temporariamente em disco
        image_path = os.path.join(temp_dir, f"page_{page_num}.jpg")
        image_pil = Image.fromarray(image_np)
        image_pil.save(image_path)

        # Carregar a imagem novamente em escala de cinza
        image_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # Aplicar a segmentação de imagem para identificar as regiões de texto
        _, binary_image = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary_image, connectivity=8)

        # Desenhar retângulos ao redor das regiões de texto na imagem original
        for i, stat in enumerate(stats[1:]):
            x, y, width, height, area = stat
            cv2.rectangle(image_np, (x, y), (x + width, y + height), (0, 255, 0), 2)

            # Recortar a região de texto da imagem original
            text_region = image_gray[y:y+height, x:x+width]

            # Realizar o OCR na região de texto usando o Tesseract
            text = pytesseract.image_to_string(text_region, lang='eng')

            # Imprimir o texto extraído
            print("Texto na região {}: {}".format(i+1, text))

        # Exibir a imagem com as regiões de texto destacadas
        cv2.imshow('Segmented Image', image_np)
        cv2.waitKey(0)

    # Fechar o arquivo PDF
    doc.close()

    # Remover o diretório temporário
    os.rmdir(temp_dir)

# Caminho para o arquivo PDF
pdf_path = 'imgs/pdf02.pdf'

# Segmentar o PDF e identificar as regiões de texto
segment_pdf(pdf_path)
