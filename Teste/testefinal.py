import os
import re
import time
import pickle
import PyPDF2
import pytesseract
from PIL import Image
from flask import Flask, request, jsonify
from validate_docbr import CPF
from nameparser import HumanName
# A primeira ativação do código é demorada e é gerada um arquivo Cache no computador, depois disso o código starta rápido. 
# É necessário fazer a instalação do Tesseract além das bibliotecas para o código funcionar
# Tem que fazer a mudança dos caminhos tanto das variáveis caminho_tesseract quanto da variável pasta_pdf
# Cuidado ao fazer o caminho da variável pasta_pdf pois ela é a pasta raiz, ela percorrerá todas as pastas que encontrar a partir daquele ponto até encontrar todos os pdf que conseguir
# É necessário utilizar algum programa auxiliar para conseguir fazer os testers dos endpoint como o Postman
# Depois da primeira ativação e alocação no cache precisa fazer a utilização do endpoint atualizar-cache, para exclusão o endpoint excluir-cache
# Esse programa unicamente procura por arquivos .pdf abrindo-os e os lendo, ele procurará dentro de qualquer pasta que encontrar mas só isso. 
app = Flask(__name__)
# Configuração do caminho para o executável do Tesseract
caminho_tesseract = r'C:\Users\wallace.santos\Desktop\Tesseract'
pytesseract.pytesseract.tesseract_cmd = f"{caminho_tesseract} -l por"

# Definir o nome do arquivo de cache
cache_file = 'cache.pkl'

# Tempo de início da execução do código
tempo_inicio = time.time()

def formatar_tempo(segundos):
    minutos = int(segundos // 60)
    segundos %= 60
    return f"{minutos} minutos e {segundos:.2f} segundos"

def cache_valido(cache_path):
    return os.path.exists(cache_path)

def carregar_ou_gerar_cache(cache_file, gerar_dados_cache):
    if cache_valido(cache_file):
        with open(cache_file, 'rb') as cache:
            return pickle.load(cache)
    else:
        caches = gerar_dados_cache()
        with open(cache_file, 'wb') as cache:
            pickle.dump(caches, cache)
        return caches

def extrair_texto_de_pdf(caminho_pdf):
    try:
        with open(caminho_pdf, 'rb') as arquivo:
            leitor_pdf = PyPDF2.PdfReader(arquivo)
            texto_extraido = ''
            for numero_pagina in range(len(leitor_pdf.pages)):
                objeto_pagina = leitor_pdf.pages[numero_pagina]
                texto_pagina = objeto_pagina.extract_text()
                texto_extraido += texto_pagina
            return texto_extraido
    except Exception as e:
        print(f"Erro ao ler o arquivo PDF '{caminho_pdf}': {e}")
        return None

def gerar_dados_cache():
    caches = {}
    pasta_pdf = r'C:\Users\wallace.santos\Documents\API_PM - Copia\Arquivos_Teste'

    for root, _, files in os.walk(pasta_pdf):
        for file in files:
            if file.lower().endswith('.pdf'):
                caminho_pdf = os.path.join(root, file)
                texto_extraido = extrair_texto_de_pdf(caminho_pdf)
                caminho_relativo = os.path.relpath(caminho_pdf, pasta_pdf)

                if root not in caches:
                    caches[root] = []
                caches[root].append((caminho_relativo, texto_extraido))

    return caches

def extrair_texto_de_imagem(caminho_imagem):
    imagem = Image.open(caminho_imagem)
    texto = pytesseract.image_to_string(imagem)
    return texto

def extrair_textos_de_pastas(pasta_raiz):
    caches = {}

    for root, _, files in os.walk(pasta_raiz):
        for file in files:
            if file.lower().endswith('.pdf'):
                caminho_pdf = os.path.join(root, file)
                texto_extraido = extrair_texto_de_pdf(caminho_pdf)
                caminho_relativo = os.path.relpath(caminho_pdf, pasta_raiz)

                if root not in caches:
                    caches[root] = []
                caches[root].append((caminho_relativo, texto_extraido))

    return caches

def ajustar_frase(frase):
    if frase is None:
        return ""
    return re.sub(r'[^0-9a-zA-Z]+', '', frase).lower()

def realizar_busca(dados, busca_tipo):
    if 'Buscar' not in dados:
        return jsonify({'erro': f'O campo "Buscar" é obrigatório para busca de {busca_tipo}.'}), 400

    frase_desejada = dados['Buscar']
    resultados = []

    caches = carregar_ou_gerar_cache(cache_file, gerar_dados_cache)
    frase_ajustada = ajustar_frase(frase_desejada)

    for pasta_pdf, entradas in caches.items():
        for caminho_pdf, texto_extraido in entradas:
            if frase_ajustada in ajustar_frase(texto_extraido):
                resultados.append(os.path.basename(os.path.normpath(caminho_pdf)))

    caminho_imagem = dados.get('caminho_imagem')
    if caminho_imagem:
        try:
            imagens_cache = None

            for imagem in imagens_cache:
                texto_extraido_imagem = extrair_texto_de_imagem(imagem)
                if frase_ajustada in ajustar_frase(texto_extraido_imagem):
                    resultados.append('Imagem')
                    break

        except Exception as e:
            print(f"Erro ao processar a imagem: {e}")

    if resultados:
        resultados = list(set(resultados))
        resultados = sorted(resultados)
        return jsonify(resultados)
    else:
        return jsonify({'mensagem': f'Nenhum resultado encontrado para a busca de {busca_tipo}.'}), 404

@app.route('/Pesquisar', methods=['POST'])
def buscar():
    return realizar_busca(request.get_json(), 'texto')

@app.route('/cpf', methods=['POST'])
def buscar_cpf():
    dados = request.get_json()
    cpf = dados['Buscar']
    if not CPF().validate(cpf):
        return jsonify({'erro': 'CPF inválido.'}), 400
    return realizar_busca(dados, 'CPF')

@app.route('/nome', methods=['POST'])
def buscar_nome():
    dados = request.get_json()
    nome = dados['Buscar']
    if not HumanName(nome).first or not HumanName(nome).last:
        return jsonify({'erro': 'Nome inválido ou incompleto.'}), 400
    return realizar_busca(dados, 'nome')

@app.route('/busca-completa', methods=['POST'])
def busca_completa():
    dados = request.get_json()
    
    if 'termo' not in dados:
        return jsonify({'erro': 'O campo "termo" é obrigatório.'}), 400
    
    termo = dados['termo']
    tipo_arquivo = dados.get('tipo_arquivo')
    ano = dados.get('ano')
    
    resultados = []
    
    caches = carregar_ou_gerar_cache(cache_file, gerar_dados_cache)
    termo_ajustado = ajustar_frase(termo)
    
    for pasta, entradas in caches.items():
        for caminho_pdf, texto_extraido in entradas:
            if (not tipo_arquivo or tipo_arquivo.isspace() or tipo_arquivo in caminho_pdf) and termo_ajustado in ajustar_frase(texto_extraido):
                if ano is None:
                    resultados.append(caminho_pdf)
                else:
                    ano_encontrado = re.search(r'\d{4}(?=(\.pdf|\s))', caminho_pdf)
                    if ano_encontrado:
                        ano_encontrado = int(ano_encontrado.group())
                        if ano == ano_encontrado:
                            resultados.append(caminho_pdf)

    if resultados:
        resultados = list(set(resultados))
        resultados = sorted(resultados)
        return jsonify(resultados)
    else:
        return jsonify({'mensagem': 'Nenhum resultado encontrado para a busca desejada.'}), 404

@app.route('/atualizar-cache', methods=['POST'])
def atualizar_cache():
    dados = request.get_json()

    if 'caminho_pasta' not in dados:
        return jsonify({'erro': 'O campo "caminho_pasta" é obrigatório.'}), 400

    caminho_pasta = dados['caminho_pasta']

    if not os.path.exists(caminho_pasta):
        return jsonify({'erro': 'O caminho da pasta raiz não é válido.'}), 400

    caches = carregar_ou_gerar_cache(cache_file, gerar_dados_cache)
    novos_caches = extrair_textos_de_pastas(caminho_pasta)

    for pasta_pdf, entradas in novos_caches.items():
        if pasta_pdf not in caches:
            caches[pasta_pdf] = []

        for caminho_pdf, texto_extraido in entradas:
            caminho_relativo = caminho_pdf
            if all(caminho_relativo != c for c, _ in caches[pasta_pdf]):
                caches[pasta_pdf].append((caminho_relativo, texto_extraido))

    with open(cache_file, 'wb') as cache:
        pickle.dump(caches, cache)

    return jsonify({'mensagem': 'Cache atualizado com sucesso.'})

@app.route('/excluir-cache/<nome_arquivo>', methods=['DELETE'])
def excluir_cache(nome_arquivo):
    if cache_valido(cache_file):
        with open(cache_file, 'rb') as cache:
            caches = pickle.load(cache)
    else:
        caches = {}

    for pasta, entradas in caches.items():
        for caminho_pdf, _ in entradas:
            if nome_arquivo in caminho_pdf:
                entradas = [e for e in entradas if nome_arquivo not in e[0]]
                caches[pasta] = entradas

    with open(cache_file, 'wb') as cache:
        pickle.dump(caches, cache)

    return jsonify({'mensagem': f'Arquivo {nome_arquivo} excluído com sucesso do cache.'})

tempo_decorrido = time.time() - tempo_inicio
print(f"Tempo até o código ser iniciado: {formatar_tempo(tempo_decorrido)}")

if __name__ == '__main__':
    app.run(debug=True)
