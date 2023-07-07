import cv2
import pytesseract
import PyPDF2

def ocr_pdf(pdf_path):
    # abrindo pdf
	with open(pdf_path, 'rb') as file:
		# criando objeto pdf reader
		pdf_reader = PyPDF2.PdfReader(file)

		#var pra guardar texto extraido
		text_extraido =''

		#iterar nas paginas do pdf
		for page_number in range(len(pdf_reader.pages)):
			# pegando o objeto da pagina atual
			page_object = pdf_reader.pages[page_number]

			# extraindo o texto da pagina
			page_text = page_object.extract_text()

			# alocando texto extraido pro resultado final
			text_extraido += page_text

	# retornando texto extraido final
	return text_extraido

#caminho do pdf
pdf_path = 'imgs/pdf04.pdf'

# executando função pra ler e extrairi texto do pdf
text_extraido = ocr_pdf(pdf_path)

# exibindo texto extraido
print(text_extraido)
