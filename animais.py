from flask import Blueprint, request, render_template
from init import ManagerCSV

GET, POST = 'GET', 'POST'

animais_bp = Blueprint('animais', __name__)

@animais_bp.route('/animal_entrada', methods= [GET, POST])
def animal_entrada():
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
