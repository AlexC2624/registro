from flask import Flask, render_template, request, redirect, url_for
from models import ManagerCSV
import os

app = Flask(__name__)

GET, POST = 'GET', 'POST'

os.makedirs('data', exist_ok=True)

@app.route('/', methods= [GET, POST])
def index():
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
    if request.method == POST:
        acao = request.form.get('acao')
        print(acao)
        if acao == 'botao1':
            return render_template('teste.html')

    return render_template('lote_cadastro.html')

@app.route('/animal_entrada', methods= [GET, POST])
def animal_entrada():
    lote = ['lote 1', 'lote 2']
    raca = ['raca 1', 'raca 2']
    fornecedor = ['fornecedor 1', 'fornecedor 2']
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

    return render_template('animal_entrada.html',
                           lote = lote,
                           raca = raca,
                           fornecedor = fornecedor,
                           status = status)
