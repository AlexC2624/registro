import os
from models import ManagerCSV
from flask import Flask, render_template, request, redirect, url_for
from flasgger import Swagger

app = Flask(__name__)   # Inicia o app do flask
Swagger(app)

GET, POST = 'GET', 'POST'   # É para evitar erro de digitação

os.makedirs('data', exist_ok=True)  # Cria a pasta se não existir para os dados

@app.route('/', methods= [GET, POST])   # Rota index
def index():
    """
    Página inicial do sistema.
    ---
    methods:
      - GET
      - POST
    parameters:
      - name: acao
        in: formData
        type: string
        required: false
        enum: ['lote_cadastro', 'animal_entrada']
        description: Ação a ser executada
    responses:
      200:
        description: Página inicial carregada
    """
    if request.method == POST:
        acao = request.form.get('acao')
        if acao == 'lote_cadastro':
            return redirect(url_for('lote_cadastro'))
        if acao == 'animal_entrada':
            return redirect(url_for('animal_entrada'))
    return render_template('index.html')

@app.route('/teste')
def teste():
    """
    Teste de rota Swagger.
    ---
    responses:
      200:
        description: Página de teste carregada
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: "API funcionando com Swagger!"
    """
    return render_template('teste.html', t=None)

@app.route('/lote_cadastro', methods= [GET, POST])
def lote_cadastro():
    """
    Cadastro de lotes.
    ---
    methods:
      - GET
      - POST
    parameters:
      - name: acao
        in: formData
        type: string
        required: false
        enum: ['botao1']
        description: Ação executada no formulário
    responses:
      200:
        description: Página de cadastro de lote renderizada
    """
    if request.method == POST:
        acao = request.form.get('acao')
        print(acao)
        if acao == 'botao1':
            return render_template('teste.html')

    return render_template('lote_cadastro.html')

@app.route('/animal_entrada', methods= [GET, POST])
def animal_entrada():
    """
    Cadastro de entrada de animais.
    ---
    methods:
      - GET
      - POST
    parameters:
      - name: lote
        in: formData
        type: string
        required: true
      - name: raca
        in: formData
        type: string
        required: true
      - name: data_nascimento
        in: formData
        type: string
        required: true
      - name: fornecedor
        in: formData
        type: string
        required: true
      - name: data_entrada
        in: formData
        type: string
        required: true
      - name: peso_entrada
        in: formData
        type: string
        required: true
      - name: valor_entrada
        in: formData
        type: string
        required: true
    responses:
      200:
        description: Página de entrada de animais renderizada
    """
    lote_opcoes = ['lote 1', 'lote 2']
    raca_opcoes = ['raca 1', 'raca 2']
    fornecedor_opcoes = ['fornecedor 1', 'fornecedor 2']
    status = None

    if request.method == POST:
        lote = request.form['lote']
        raca = request.form['raca']
        data_nascimento = request.form['data_nascimento']
        fornecedor = request.form['fornecedor']
        data_entrada = request.form['data_entrada']
        peso_entrada = request.form['peso_entrada']
        valor_entrada = request.form['valor_entrada']

        # Caminho do arquivo CSV
        arquivo = 'data/animal_entrada.csv'

        # Criar dicionário com os dados recebidos
        novo_animal = {
            'lote': lote,
            'raca': raca,
            'data_nascimento': data_nascimento,
            'fornecedor': fornecedor,
            'data_entrada': data_entrada,
            'peso_entrada': peso_entrada,
            'valor_entrada': valor_entrada
        }

        # Verifica se o arquivo já existe
        banco = ManagerCSV(arquivo, list(novo_animal.keys()))
        banco.adicionar(novo_animal)

        status = 'Salvo com sucesso!'

    return render_template(
        'animal_entrada.html',
        lote_opcoes = lote_opcoes,
        raca_opcoes = raca_opcoes,
        fornecedor_opcoes = fornecedor_opcoes,
        status = status
    )

@app.route('/tos')
def tos():
    """
    Exibe os Termos de Serviço.
    ---
    responses:
      200:
        description: Retorna os termos de serviço.
        schema:
          type: object
          properties:
            termos:
              type: string
              example: "Aqui estão os termos de serviço."
    """
    return render_template('tos.html')
