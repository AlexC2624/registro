import os
from models import ManagerCSV
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)   # Inicia o app do flask

from app.animais import animais_bp
app.register_blueprint(animais_bp, url_prefix='/animais')

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
