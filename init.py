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
    return render_template('tos.html')

@app.route('/cadastros', methods= [GET, POST])
def cadastros():
    if request.method == POST:
        json_categoria = request.form.get('json_categoria')
        if json_categoria:
            return redirect(url_for('json_animal', categoria=json_categoria))

        animal = request.form.get('animal')
        if animal:
            return redirect(url_for('animal', modo=animal))

        insumo = request.form.get('insumo')
        if insumo: return redirect(url_for('insumo', modo=insumo))

        manejo = request.form.get('manejo')
        if manejo: return redirect(url_for('manejo', modo=manejo))

    return render_template('cadastros.html')

@app.route('/json_animal/<categoria>', methods= [GET, POST])
def json_animal(categoria):
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
            qtd_animais_entrada = int(request.form['qtd_animais_entrada'])

            # Caminho do arquivo CSV
            arquivo = 'animal_entrada.csv'

            banco = ManagerCSV(arquivo, [
                'lote', 'raca', 'data_nascimento', 'fornecedor',
                'data_entrada', 'peso_entrada', 'valor_entrada'
            ])
            proximo_id = False
            if banco.linhas() == 0:
                banco2 = ManagerCSV('animal_saida.csv')
                if banco2.linhas() != 0:
                    proximo_id = banco2.ler()['valores'][-1][1] + 1

            for _ in range(qtd_animais_entrada):
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
                if proximo_id: banco.adicionar(novo_registro, proximo_id)
                else: banco.adicionar(novo_registro)

            status = 'Salvo com sucesso!'

        # Verifica se há lotes cadastrados
        lote_opcoes = json.obter_dado('lote')
        if lote_opcoes == {}:
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
            idx_entrada = request.form.getlist('animaisSelecionados[]')  # Agora é uma lista
            cliente = request.form['cliente']
            data_saida = request.form['data_saida']
            peso_saida = request.form['peso_saida']
            valor_saida = request.form['valor_saida']
            # print(idx_entrada, cliente, data_saida, peso_saida, valor_saida, sep='\n')

            # Caminho do arquivo CSV
            arquivo = 'animal_entrada.csv'
            banco_entrada = ManagerCSV(arquivo)
            # Verifica se há entradas de animais
            if banco_entrada.linhas() == 0:
                status = 'Nenhum animal cadastrado para saída'
                return render_template('animal.html', status=status)
            
            # Lê os dados de entrada
            dados_entrada = banco_entrada.ler()['valores']

            # Caminho do arquivo CSV
            arquivo = 'animal_saida.csv'
            colunas = ['idx_entrada','lote','raca', 'data_nascimento', 'fornecedor',
                       'data_entrada', 'peso_entrada', 'valor_entrada', 'cliente',
                       'data_saida', 'peso_saida', 'valor_saida']
            banco_saida = ManagerCSV(arquivo, colunas)

            for idx in idx_entrada:
                idx = int(idx)  # Converte o ID para inteiro
                for linha in dados_entrada:
                    if linha[0] == idx:  # Busca a linha correspondente ao ID
                        # Criar dicionário com os dados recebidos
                        novo_registro = {
                            # Valores de entrada
                            'idx_entrada': linha[0],
                            'lote': linha[1],
                            'raca': linha[2],
                            'data_nascimento': linha[3],
                            'fornecedor': linha[4],
                            'data_entrada': linha[5],
                            'peso_entrada': linha[6],
                            'valor_entrada': linha[7],
                            # Valores de saída
                            'cliente': cliente,
                            'data_saida': data_saida,
                            'peso_saida': peso_saida,
                            'valor_saida': valor_saida
                        }

                        banco_saida.adicionar(novo_registro)

                banco_entrada.excluir(idx)  # Remove a entrada do animal após registro do mesmo na saída

            status = 'Salvo com sucesso!'
        
        # Verifica se há lote cadastrado
        lote = json.obter_dado('lote')
        if lote == []:
            status = 'Nenhum lote de animais cadastrado'
            return render_template('animal.html', status=status)
        
        # Verifica se há entrada de animal
        animal_entrada = ManagerCSV('animal_entrada.csv')
        if animal_entrada.linhas() == 0:
            status = 'Nenhum animal cadastrado' if not status else status
            return render_template('animal.html', status=status)
        animal_entrada = animal_entrada.ler()
        animal_entrada = animal_entrada['valores']
        
        # Verifica se há saída de animal
        animal_saida = ManagerCSV('animal_saida.csv')
        if animal_saida.linhas() > 0:
            animal_saida = animal_saida.ler()['valores']
            saida_ids = [saida[1] for saida in animal_saida]
            animal_entrada = [entrada for entrada in animal_entrada if entrada[0] not in saida_ids]

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
            animal_entrada_opcoes = animal_entrada if animal_entrada else None,
            cliente_opcoes = cliente_opcoes
        )

@app.route('/insumo/<modo>', methods=[GET, POST])
def insumo(modo):
    status = None
    modo = modo
    insumo_opcoes = None
    lote_opcoes = None
    fornecedor_opcoes = None

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
                'estoque': 0,  # Inicializa o estoque como 0
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
            insumo = request.form['insumo']
            data = request.form['data']
            quantidade = request.form['quantidade']
            valor_unitario = request.form['valor_unitario']

            # Criar dicionário com os dados recebidos
            novo_registro = {
                'insumo': insumo,
                'data': data,
                'quantidade': quantidade,
                'valor_unitario': valor_unitario
            }

            # Caminho do arquivo CSV correto
            arquivo = 'insumo_comprado.csv'

            banco = ManagerCSV(arquivo, list(novo_registro.keys()))
            banco.adicionar(novo_registro)

            # Atualiza o estoque do insumo
            insumo_dados = json_insumo.obter_dado('insumo', insumo)
            insumo_dados['estoque'] += int(quantidade)
            json_insumo.editar_dado('insumo', insumo, insumo_dados)

            status = 'Compra registrada com sucesso!'

        insumo_opcoes = json_insumo.obter_dado('insumo')
        if insumo_opcoes == {}:
            status = 'Nenhum insumo cadastrado'
            return render_template('insumo.html', status=status)

    return render_template(
        'insumo.html',
        status = status,
        modo = modo,
        insumo_opcoes = insumo_opcoes,
        lote_opcoes = lote_opcoes,
        fornecedor_opcoes = fornecedor_opcoes,
    )

@app.route('/manejo/<modo>', methods=[GET, POST])
def manejo(modo):
    status = None
    insumo_opcoes = None
    lote_opcoes = None
    animal_opcoes = None
    json_animais = ManagerJSON('animais.json')
    json_insumo = ManagerJSON('insumos.json')

    if modo == 'alimentacao':
        if request.method == POST:
            insumo = request.form['insumo']
            lote_opcoes = json_animais.obter_dado('lote')
            data_inicio = request.form['data_inicio']
            data_fim = request.form['data_fim']
            quantidade = request.form['quantidade']
            observacao = request.form['observacao']

            novo_registro = {
                'insumo': insumo,
                'lote': lote_opcoes,
                'data_inicio': data_inicio,
                'data_fim': data_fim,
                'quantidade': quantidade,
                'observacao': observacao
            }

            # Caminho do arquivo CSV para consumo
            arquivo = 'insumo_consumo.csv'

            banco = ManagerCSV(arquivo, list(novo_registro.keys()))
            banco.adicionar(novo_registro)

            # Atualiza o estoque do insumo
            insumo_dados = json_insumo.obter_dado('insumo', insumo)
            insumo_dados['estoque'] -= int(quantidade)
            json_insumo.editar_dado('insumo', insumo, insumo_dados)

            status = 'Consumo registrado com sucesso!'

        insumo_opcoes = json_insumo.obter_dado('insumo')
        if insumo_opcoes == {}:
            status = 'Nenhum insumo cadastrado'
            return render_template('manejo.html', status=status)
        
        lote_opcoes = json_animais.obter_dado('lote')
        if lote_opcoes == {}:
            status = 'Nenhum lote cadastrado'
            return render_template('manejo.html', status=status)

    elif modo == 'pesagem':
        if request.method == POST:
            lote = request.form['lote']
            data = request.form['data']
            peso = request.form['peso']
            observacao = request.form['observacao']

            novo_registro = {
                'lote': lote,
                'data': data,
                'peso': peso,
                'observacao': observacao
            }

            # Caminho do arquivo CSV para pesagem
            arquivo = 'animal_pesagem.csv'

            banco = ManagerCSV(arquivo, list(novo_registro.keys()))
            banco.adicionar(novo_registro)

            status = 'Pesagem registrada com sucesso!'

        lote_opcoes = json_animais.obter_dado('lote')
        if lote_opcoes == {}:
            status = 'Nenhum lote cadastrado'
            return render_template('manejo.html', status=status)
        
        insumo_opcoes = json_insumo.obter_dado('insumo')
        if insumo_opcoes == {}:
            status = 'Nenhum insumo cadastrado'
            return render_template('manejo.html', status=status)
        
        animal_opcoes = json_animais.obter_dado('animal')
        if animal_opcoes == {}:
            status = 'Nenhum animal cadastrado'
            return render_template('manejo.html', status=status)

    return render_template(
        'manejo.html',
        status = status,
        modo = modo,
        insumo_opcoes = insumo_opcoes,
        lote_opcoes = lote_opcoes,
        animal_opcoes = animal_opcoes
    )

@app.route('/relatorios', methods=[GET, POST])
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
