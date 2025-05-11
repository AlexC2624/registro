import os
from models import ManagerCSV
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)   # Inicia o app do flask

GET, POST = 'GET', 'POST'   # É para evitar erro de digitação

os.makedirs('data', exist_ok=True)  # Cria a pasta se não existir para os dados

@app.route('/', methods= [GET, POST])   # Rota index
def index():
    """
    Função responsável por renderizar a página inicial do sistema. Ela verifica o método de requisição
    (GET ou POST) e, se for um POST, redireciona o usuário para as rotas apropriadas com base na ação 
    selecionada. Se a ação for 'lote_cadastro', o usuário é redirecionado para o cadastro de lote.
    Se a ação for 'animal_entrada', o usuário é redirecionado para a entrada de animais.

    Se o método de requisição for GET, a função apenas renderiza a página inicial.

    Retorna:
        - render_template('index.html'): Página inicial renderizada se o método for GET.
        - redirect(url_for('lote_cadastro')): Redireciona para a página de cadastro de lote se a ação for 'lote_cadastro'.
        - redirect(url_for('animal_entrada')): Redireciona para a página de entrada de animais se a ação for 'animal_entrada'.
    """
    if request.method == POST:
        acao = request.form.get('acao')
        if acao == 'lote_cadastro':
            return redirect(url_for('lote_cadastro'))
        if acao == 'animal_entrada':
            return redirect(url_for('animal_entrada'))
    return render_template('index.html')

@app.route('/teste')
def teste(): return render_template('teste.html', t=None)

@app.route('/lote_cadastro', methods= [GET, POST])
def lote_cadastro():
    """
    Função responsável por gerenciar o cadastro de lotes. Se o método de requisição for POST, ela verifica
    a ação enviada pelo formulário. Se a ação for 'botao1', a função renderiza uma página de teste. Caso contrário,
    a função exibe a página de cadastro de lote.

    Se o método de requisição for GET, a função renderiza a página de cadastro de lote.

    Retorna:
        - render_template('teste.html'): Página de teste renderizada caso a ação seja 'botao1'.
        - render_template('lote_cadastro.html'): Página de cadastro de lote renderizada se o método for GET ou 
          se a ação não for 'botao1'.
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
    Função responsável por gerenciar o cadastro de entrada de animais no sistema. Quando o método de requisição 
    é POST, ela recebe os dados do formulário de entrada do animal, como lote, raça, data de nascimento, fornecedor,
    data de entrada, peso de entrada e valor de entrada. Esses dados são armazenados em um arquivo CSV.

    Se o método for GET, a função exibe o formulário para cadastro de um novo animal com as opções de lote, raça
    e fornecedor. Após a submissão do formulário, o sistema verifica se o arquivo CSV existe e, se não, cria um 
    novo registro com os dados fornecidos.

    Parâmetros:
        - lote_opcoes (list): Lista de opções de lotes disponíveis.
        - raca_opcoes (list): Lista de opções de raças disponíveis.
        - fornecedor_opcoes (list): Lista de opções de fornecedores disponíveis.
        - status (str): Mensagem de status que será exibida após o cadastro (exemplo: "Salvo com sucesso!").

    Retorna:
        - render_template('animal_entrada.html'): Página de entrada de animais renderizada com as opções de 
          lote, raça, fornecedor e o status de cadastro.
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
