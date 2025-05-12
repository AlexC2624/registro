import os
from models import ManagerCSV, ManagerJSON
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
        enum: ['lote_animal', 'animal_entrada']
        description: Ação a ser executada
    responses:
      200:
        description: Página inicial carregada
    """
    if request.method == POST:
        acao = request.form.get('acao')
        # if acao == 'lote_animal': return redirect(url_for('lote_animal'))
        if acao == 'animal_entrada': return redirect(url_for('animal_entrada'))
        if acao == 'animal_saida': return redirect(url_for('animal_saida'))
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

@app.route('/json_animal/<categoria>', methods= [GET, POST])
def json_animal(categoria):
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
        enum: ['voltar', 'cadastrar']
        description: Ação executada no formulário ('voltar' retorna à página inicial, 'cadastrar' registra o novo lote)
      - name: nome
        in: formData
        type: string
        required: false
        description: Nome do lote a ser cadastrado
    responses:
      200:
        description: Página de cadastro de lote renderizada com ou sem mensagem de status
    """
    status = None
    if request.method == POST:
        nome = request.form.get('nome')
        if nome:
            json = ManagerJSON('animais.json')
            json.atualizar_dado(categoria, {'nome': nome if type(nome) is str else str(nome)})
            status = f'Lote {nome} cadastrado!'
        return render_template('cadastro_json_animais.html', categoria=categoria, status=status)

    return render_template('cadastro_json_animais.html', categoria=categoria, status=status)

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
    lote_opcoes = ManagerJSON('animais.json')
    lote_opcoes = lote_opcoes.obter_dado('lote')
    lote_opcoes = [lote_opcoes[i]['nome'] for i in lote_opcoes.keys()]
    if lote_opcoes == []:
        status = 'Nenhum lote de animais cadastrado'
        return render_template('animal_entrada.html', status=status)

    raca_opcoes = ManagerJSON('animais.json')
    raca_opcoes = raca_opcoes.obter_dado('raca')
    raca_opcoes = [raca_opcoes[i]['nome'] for i in raca_opcoes.keys()]
    if raca_opcoes == []:
        status = 'Nenhuma raca de animais cadastrado'
        return render_template('animal_entrada.html', status=status)

    fornecedor_opcoes = ManagerJSON('animais.json')
    fornecedor_opcoes = fornecedor_opcoes.obter_dado('fornecedor')
    fornecedor_opcoes = [fornecedor_opcoes[i]['nome'] for i in fornecedor_opcoes.keys()]
    if fornecedor_opcoes == []:
        status = 'Nenhum fornecedor de animais cadastrado'
        return render_template('animal_entrada.html', status=status)
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

@app.route('/animal_saida', methods= [GET, POST])
def animal_saida():
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
    cliente_opcoes = ManagerJSON('animais.json')
    cliente_opcoes = cliente_opcoes.obter_dado('cliente')
    cliente_opcoes = [cliente_opcoes[i]['nome'] for i in cliente_opcoes.keys()]
    if cliente_opcoes == []:
        status = 'Nenhum cliente de animal cadastrado'
        return render_template('animal_saida.html', status=status)
    
    status = None

    if request.method == POST:
        idx_entrada = request.form['idx_entrada']
        cliente = request.form['cliente']
        data_saida = request.form['data_saida']
        peso_saida = request.form['peso_saida']
        valor_saida = request.form['valor_saida']

        # Caminho do arquivo CSV
        arquivo = 'data/animal_saida.csv'

        # Criar dicionário com os dados recebidos
        novo_animal = {
            'idx_entrada': idx_entrada,
            'cliente': cliente,
            'data_saida': data_saida,
            'peso_saida': peso_saida,
            'valor_saida': valor_saida
        }

        # Verifica se o arquivo já existe
        banco = ManagerCSV(arquivo, list(novo_animal.keys()))
        banco.adicionar(novo_animal)

        status = 'Salvo com sucesso!'

    return render_template(
        'animal_saida.html',
        cliente_opcoes = cliente_opcoes,
        status = status
    )
