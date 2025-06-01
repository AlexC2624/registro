import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import joblib
import os

class RegressaoPolinomial:
    def __init__(self, grau=3, caminho_modelo='modelo_poly.pkl'):
        """
        Inicializa o modelo de regressão polinomial.

        :param grau: Grau do polinômio para transformação dos dados.
        :param caminho_modelo: Caminho para salvar/carregar o modelo treinado.
        """
        self.grau = grau
        self.poly = PolynomialFeatures(degree=grau)
        self.modelo = LinearRegression()
        self.caminho_modelo = caminho_modelo
        self.treinado = False
    
    def carregar_dados(self, caminho_csv):
        """
        Carrega dados do arquivo CSV.

        :param caminho_csv: Caminho do arquivo CSV com colunas 'diametro' e 'preco'.
        """
        self.df = pd.read_csv(caminho_csv)
    
    def treinar(self, df=None, incremental=False):
        """
        Treina o modelo.

        :param df: DataFrame com dados. Se None, usa dados já carregados.
        :param incremental: Se True, faz treino incremental (refit com dados antigos + novos).
        """
        if df is not None:
            dados = df
        elif hasattr(self, 'df'):
            dados = self.df
        else:
            raise ValueError("Nenhum dado fornecido para treinamento.")
        
        X_poly = self.poly.fit_transform(dados[['diametro']])
        y = dados[['preco']]
        
        if incremental and self.treinado:
            # Treinamento incremental simulando: concatenar dados antigos + novos
            # Re-treinar modelo com dados antigos + novos
            # Para simplificar, se desejar treino incremental real, é melhor usar modelos que suportem partial_fit.
            dados_antigos = self.df if hasattr(self, 'df') else pd.DataFrame(columns=['diametro', 'preco'])
            dados_completos = pd.concat([dados_antigos, dados]).drop_duplicates().reset_index(drop=True)
            X_poly = self.poly.fit_transform(dados_completos[['diametro']])
            y = dados_completos[['preco']]
            self.df = dados_completos  # Atualiza dados usados
            self.modelo.fit(X_poly, y)
        else:
            self.modelo.fit(X_poly, y)
            self.df = dados  # Salva dados para possível treino incremental
        self.treinado = True
    
    def salvar_modelo(self):
        """
        Salva o modelo e o transformador polinomial em arquivo.
        """
        joblib.dump({
            'modelo': self.modelo,
            'poly': self.poly,
            'grau': self.grau,
            'df': getattr(self, 'df', None)
        }, self.caminho_modelo)
        print(f'Modelo salvo em {self.caminho_modelo}')
    
    def carregar_modelo(self):
        """
        Carrega o modelo salvo e o transformador polinomial.
        """
        if not os.path.exists(self.caminho_modelo):
            raise FileNotFoundError(f'Arquivo {self.caminho_modelo} não encontrado.')
        dados = joblib.load(self.caminho_modelo)
        self.modelo = dados['modelo']
        self.poly = dados['poly']
        self.grau = dados['grau']
        self.df = dados['df']
        self.treinado = True
        print(f'Modelo carregado de {self.caminho_modelo}')
    
    def prever(self, diametro):
        """
        Realiza a previsão do preço para um dado diâmetro.

        :param diametro: Valor do diâmetro para prever o preço.
        :return: Preço previsto (float).
        """
        if not self.treinado:
            raise RuntimeError("Modelo não treinado. Treine ou carregue um modelo antes de prever.")
        X_poly = self.poly.transform(pd.DataFrame({'diametro': [diametro]}))
        preco_previsto = self.modelo.predict(X_poly)
        return preco_previsto[0][0]
    
    def plotar(self):
        """
        Plota os dados reais e a curva da regressão polinomial.
        """
        if not self.treinado:
            raise RuntimeError("Modelo não treinado. Treine ou carregue um modelo antes de plotar.")
        
        plt.scatter(self.df['diametro'], self.df['preco'], color='blue', label='Dados Reais')
        # Ordenar para plotagem suave da curva
        X_plot = pd.DataFrame({'diametro': sorted(self.df['diametro'])})
        X_poly_plot = self.poly.transform(X_plot)
        y_pred = self.modelo.predict(X_poly_plot)
        plt.plot(X_plot['diametro'], y_pred, color='red', label=f'Regressão Polinomial (grau {self.grau})')
        plt.xlabel('Diâmetro')
        plt.ylabel('Preço')
        plt.title('Regressão Polinomial - Preço x Diâmetro')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    def avaliar(self):
        """
        Calcula e retorna o coeficiente de determinação R².

        :return: R² do modelo (float).
        """
        if not self.treinado:
            raise RuntimeError("Modelo não treinado. Treine ou carregue um modelo antes de avaliar.")
        X_poly = self.poly.transform(self.df[['diametro']])
        y = self.df[['preco']]
        r2 = self.modelo.score(X_poly, y)
        return r2

######################################################################################
# Criar o objeto e carregar dados
reg = RegressaoPolinomial(grau=3)
reg.carregar_dados('data.csv')

# Treinar o modelo
if not reg.treinado:
    print("Treinando o modelo...")
    reg.treinar()

    # Salvar o modelo para uso futuro
    reg.salvar_modelo()

# Fazer previsão
preco = reg.prever(20)
print(f'Preço previsto para diâmetro 20: {preco:.2f}')

# Avaliar modelo
print(f'R²: {reg.avaliar():.3f}')

# Plotar os dados e a curva ajustada
reg.plotar()

# Se quiser carregar modelo salvo depois:
# reg = RegressaoPolinomial()
# reg.carregar_modelo()
# preco = reg.prever(20)

import joblib

dados = joblib.load('modelo_poly.pkl')

print(type(dados))   # para ver o tipo (geralmente dict no seu caso)
print(dados.keys())  # se for dict, para listar as chaves

for chave, valor in dados.items():
    print(f'\nChave: {chave}')
    print(f'Tipo: {type(valor)}')
    print(f'Conteúdo (resumo): {str(valor)[:500]}')  # printa os primeiros 500 caracteres para não poluir demais

modelo = dados['modelo']
print(modelo.coef_)
print(modelo.intercept_)

poly = dados['poly']
print(poly.degree)
