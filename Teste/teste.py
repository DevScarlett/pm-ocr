import os
import PyPDF2

def ocr_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text_extraido = ''
        for page_number in range(len(pdf_reader.pages)):
            page_object = pdf_reader.pages[page_number]
            page_text = page_object.extract_text()
            
            # Verificar se existem 9 dígitos de CPF seguidos de um hífen
            cpf_com_hifen = page_text.replace(" ", "").replace(".", "").replace("\n", "")
            for i in range(len(cpf_com_hifen) - 10):
                if cpf_com_hifen[i:i+9].isdigit() and cpf_com_hifen[i+9] == "-":
                    # Caso seja encontrado, unir o hífen aos dígitos do CPF
                    page_text = page_text.replace(cpf_com_hifen[i:i+10], cpf_com_hifen[i:i+9] + "-")

            text_extraido += page_text

    return text_extraido

def validar_cpf(cpf):
    cpf_numerico = ''.join(filter(str.isdigit, cpf))
    return len(cpf_numerico) == 11

pasta_pdf = r'C:\Users\wallace.santos\Documents\Teste\imgs'

textos_extraidos = []
for nome_arquivo in os.listdir(pasta_pdf):
    if nome_arquivo.lower().endswith('.pdf'):
        caminho_arquivo = os.path.join(pasta_pdf, nome_arquivo)
        texto_extraido = ocr_pdf(caminho_arquivo)
        textos_extraidos.append(texto_extraido)

def exibir_menu():
    print("Menu:")
    print("1. Ler por nome")
    print("2. Ler pelo CPF")
    print("0. Sair")

def ler_escolha():
    try:
        escolha = int(input("Digite o número da opção desejada: "))
        return escolha
    except ValueError:
        print("Entrada inválida. Por favor, digite um número.")
        return ler_escolha()

while True:
    exibir_menu()
    opcao = ler_escolha()

    if opcao == 1:
        nome = input("Você escolheu ler pelo nome.\nDigite o nome que deseja pesquisar: ")
        for idx, texto in enumerate(textos_extraidos):
            if nome in texto:
                print(f'Encontrado em {os.listdir(pasta_pdf)[idx]}')
            else:
                print(f'Não encontrado em {os.listdir(pasta_pdf)[idx]}')
        break
    elif opcao == 2:
        cpf = input("Você escolheu ler pelo CPF.\nDigite o número do CPF que deseja pesquisar: ")
        cpf_parte = cpf.replace(".", "").replace("-", "")[:9]
        for idx, texto in enumerate(textos_extraidos):
            if cpf_parte in texto.replace(".", "").replace("-", ""):
                print(f'Encontrado em {os.listdir(pasta_pdf)[idx]}')
            else:
                print(f'Não encontrado em {os.listdir(pasta_pdf)[idx]}')
        break
    elif opcao == 0:
        print("Saindo do menu.")
        break
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")
