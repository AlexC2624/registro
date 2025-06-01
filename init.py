import os
from models import ManagerCSV, ManagerJSON
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flasgger import Swagger
from funcoes_relatorios import *

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
        valor = request.form.get('page')
        if valor == 'cadastros': return redirect(url_for('cadastros'))
        if valor == 'relatorios': return redirect(url_for('relatorios'))
        if valor == 'estoque': return redirect(url_for('estoque'))
        if valor == 'financeiro': return redirect(url_for('financeiro'))

    return render_template('index.html')

@app.route('/teste', methods=["GET", "POST"])
def teste():
    if request.method == "POST":
        ids = request.form.getlist("animaisSelecionados[]")
        print(ids)  # Ex: ['1', '2']
        # Aqui você pode converter para int, consultar banco etc.
        return "IDs recebidos: " + ", ".join(ids)
    return render_template('teste.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

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

@app.route('/cadastros', methods= [GET, POST])
def cadastros():
    if request.method == POST:
        animal = request.form.get('animal')
        insumo = request.form.get('insumo')
        json_categoria = request.form.get('json_categoria')

        if json_categoria: return redirect(url_for('json_animal', categoria=json_categoria))
        elif animal: return redirect(url_for('animal', modo=animal))

        elif insumo: return redirect(url_for('insumo', modo=insumo))

    return render_template('cadastros.html')

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
            status = f'{categoria} {nome} cadastrado!'
        return render_template('cadastro_json_animais.html', categoria=categoria, status=status)

    return render_template('cadastro_json_animais.html', categoria=categoria, status=status)

@app.route('/animal/<modo>', methods= [GET, POST])
def animal(modo):
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

    status = None
    json = ManagerJSON('animais.json')

    if modo == 'entrada':
        if request.method == POST:
            lote = request.form['lote']
            raca = request.form['raca']
            data_nascimento = request.form['data_nascimento']
            fornecedor = request.form['fornecedor']
            data_entrada = request.form['data_entrada']
            peso_entrada = request.form['peso_entrada']
            valor_entrada = request.form['valor_entrada']

            # Caminho do arquivo CSV
            arquivo = 'animal_entrada.csv'

            # Criar dicionário com os dados recebidos
            novo_registro = {
                'lote': lote,
                'raca': raca,
                'data_nascimento': data_nascimento,
                'fornecedor': fornecedor,
                'data_entrada': data_entrada,
                'peso_entrada': peso_entrada,
                'valor_entrada': valor_entrada
            }

            banco = ManagerCSV(arquivo, list(novo_registro.keys()))
            banco.adicionar(novo_registro)

            status = 'Salvo com sucesso!'

        lote_opcoes = json.obter_dado('lote')

        # Verifica se há lotes cadastrados
        if lote_opcoes == []:
            status = 'Nenhum lote de animais cadastrado'
            return render_template('animal.html', status=status)

        # Verifica se há raças cadastradas
        raca_opcoes = json.obter_dado('raca')
        raca_opcoes = [raca_opcoes[i]['nome'] for i in raca_opcoes.keys()]
        if raca_opcoes == []:
            status = 'Nenhuma raca de animais cadastrado'
            return render_template('animal.html', status=status)

        # Verifica se há fornecedores cadastrados
        fornecedor_opcoes = json.obter_dado('fornecedor')
        fornecedor_opcoes = [fornecedor_opcoes[i]['nome'] for i in fornecedor_opcoes.keys()]
        if fornecedor_opcoes == []:
            status = 'Nenhum fornecedor de animais cadastrado'
            return render_template('animal.html', status=status)
        return render_template(
            'animal.html',
            modo = modo,
            lote_opcoes = lote_opcoes,
            raca_opcoes = raca_opcoes,
            fornecedor_opcoes = fornecedor_opcoes,
            status = status
        )

    elif modo == 'saida':
        if request.method == POST:
            idx_lote = request.form['idx_lote']
            idx_entrada = request.form['idx_entrada']
            cliente = request.form['cliente']
            data_saida = request.form['data_saida']
            peso_saida = request.form['peso_saida']
            valor_saida = request.form['valor_saida']

            # Caminho do arquivo CSV
            arquivo = 'animal_saida.csv'

            # Criar dicionário com os dados recebidos
            novo_registro = {
                'idx_entrada': idx_entrada,
                'cliente': cliente,
                'data_saida': data_saida,
                'peso_saida': peso_saida,
                'valor_saida': valor_saida
            }

            banco = ManagerCSV(arquivo, list(novo_registro.keys()))
            banco.adicionar(novo_registro)

            status = 'Salvo com sucesso!'
        
        # Verifica se há lote cadastrado
        lote = json.obter_dado('lote')
        if lote == []:
            status = 'Nenhum lote de animais cadastrado'
            return render_template('animal.html', status=status)
        
        # Verifica se há entrada de animal
        animal_entrada = ManagerCSV('animal_entrada.csv')
        if animal_entrada.linhas == 0:
            status = 'Nenhum animal cadastrado'
            return render_template('animal.html', status=status)
        
        animal_entrada = animal_entrada.ler()
        animal_entrada = animal_entrada['valores']

        # Verifica se há clientes cadastrados
        cliente_opcoes = json.obter_dado('cliente')
        cliente_opcoes = [cliente_opcoes[i]['nome'] for i in cliente_opcoes.keys()]
        if cliente_opcoes == []:
            status = 'Nenhum cliente de animal cadastrado'
            return render_template('animal.html', status=status)

        return render_template(
            'animal.html',
            status = status,
            modo = modo,
            lote_opcoes = lote,
            animal_entrada_opcoes = animal_entrada,
            cliente_opcoes = cliente_opcoes
        )

@app.route('/insumo/<modo>', methods=[GET, POST])
def insumo(modo):
    status = None
    json_animais = ManagerJSON('animais.json')
    json_insumo = ManagerJSON('insumos.json')
    
    if modo == 'novo':
        if request.method == POST:
            nome = request.form['nome']
            fornecedor = request.form['fornecedor']
            tipo = request.form['tipo']
            unidade = request.form['unidade']

            if not nome or not fornecedor or not tipo or not unidade:
                status = 'Preencha todos os campos!'
                return render_template('insumo.html', status=status)

            if nome in [json_insumo.obter_dado('insumo')[i]['nome'] for i in json_insumo.obter_dado('insumo').keys()]:
                status = 'O nome do insumo já existe, tente outro!'

            # Criar dicionário com os dados recebidos
            novo_registro = {
                'nome': nome,
                'fornecedor': fornecedor,
                'tipo': tipo,
                'unidade': unidade
            }
            
            if locals().get('status') is None:
                json_insumo.atualizar_dado('insumo', novo_registro)
                status = 'Insumo cadastrado com sucesso!'

        fornecedor_opcoes = json_animais.obter_dado('fornecedor')
        fornecedor_opcoes = [fornecedor_opcoes[i]['nome'] for i in fornecedor_opcoes.keys()]
        if fornecedor_opcoes == []:
            status = 'Nenhum fornecedor cadastrado'
            return render_template('insumo.html', status=status)
        
        return render_template(
            'insumo.html',
            status = locals().get('status', None),
            modo = modo,
            insumo_opcoes = None,
            fornecedor_opcoes = fornecedor_opcoes,
        )

    elif modo == 'compra':
        if request.method == POST:
            nome = request.form['nome']
            fornecedor = request.form['fornecedor']
            data_compra = request.form['data_compra']
            data_validade = request.form['data_validade']
            quantidade = request.form['quantidade']
            valor_entrada = request.form['valor_entrada']

            # Caminho do arquivo CSV correto
            arquivo = 'insumo_comprado.csv'

            # Criar dicionário com os dados recebidos
            novo_registro = {
                'nome': nome,
                'data_compra': data_compra,
                'fornecedor': fornecedor,
                'data_validade': data_validade,
                'quantidade': quantidade,
                'valor_unitario': valor_entrada
            }

            banco = ManagerCSV(arquivo, list(novo_registro.keys()))
            banco.adicionar(novo_registro)

            status = 'Compra registrada com sucesso!'

        nome_opcoes = json.obter_dado('insumo')
        nome_opcoes = [nome_opcoes[i]['nome'] for i in nome_opcoes.keys()]
        if nome_opcoes == []:
            status = 'Nenhum insumo cadastrado'
            return render_template('insumo.html', status=status)

        fornecedor_opcoes = json.obter_dado('fornecedor')
        fornecedor_opcoes = [fornecedor_opcoes[i]['nome'] for i in fornecedor_opcoes.keys()]
        if fornecedor_opcoes == []:
            status = 'Nenhum fornecedor cadastrado'
            return render_template('insumo.html', status=status)

    elif modo == 'consumo':
        if request.method == POST:
            nome = request.form['nome']
            data_consumo = request.form['data_consumo']
            quantidade = request.form['quantidade']
            observacao = request.form['observacao']

            # Caminho do arquivo CSV para consumo
            arquivo = 'insumo_consumo.csv'

            novo_registro = {
                'nome': nome,
                'data': data_consumo,
                'quantidade': quantidade,
                'observacao': observacao
            }

            banco = ManagerCSV(arquivo, list(novo_registro.keys()))
            banco.adicionar(novo_registro)

            status = 'Consumo registrado com sucesso!'

        nome_opcoes = json.obter_dado('insumo')
        nome_opcoes = [nome_opcoes[i]['nome'] for i in nome_opcoes.keys()]
        if nome_opcoes == []:
            status = 'Nenhum insumo cadastrado'
            return render_template('insumo.html', status=status)

    return render_template(
        'insumo.html',
        status = status,
        modo = modo,
        insumo_opcoes = nome_opcoes,
        fornecedor_opcoes = fornecedor_opcoes,
    )

@app.route('/relatorios', methods=['GET', 'POST'])
def relatorios():
    relatorio = None
    colunas, conteudo = "", ""

    if request.method == 'POST':
        form_animais = request.form.get('animais')
        relatorio = request.form.get('relatorio')
        if form_animais: 
            colunas, conteudo = animais(form_animais)
            print(colunas, conteudo, form_animais, sep='\n')
            relatorio = form_animais
        # elif relatorio == 'compras_insumos':
        #     colunas, conteudo = gerar_relatorio_compras_insumos()
        # elif relatorio == 'consumo_insumos':
        #     colunas, conteudo = gerar_relatorio_consumo_insumos()
        # elif relatorio == 'vendas_animais':
        #     colunas, conteudo = gerar_relatorio_vendas()
        # elif relatorio == 'balanco_geral':
        #     colunas, conteudo = gerar_relatorio_balanco()

    return render_template('relatorios.html', relatorio=relatorio, colunas=colunas, conteudo=conteudo)

@app.route('/estoque', methods= [GET, POST])
def estoque():
    # return render_template('estoque.html')
    return render_template('index.html')

@app.route('/financeiro', methods= [GET, POST])
def financeiro():
    # return render_template('financeiro.html')
    return render_template('index.html')
