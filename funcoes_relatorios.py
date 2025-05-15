from models import ManagerCSV, ManagerJSON

def animais(arquivo):
    arquivo = f'{arquivo}.csv'
    csv = ManagerCSV(arquivo)
    csv_ler = csv.ler()
    return csv_ler['colunas'], csv_ler['valores']

def gerar_relatorio_movimentacoes():
    colunas = ["Data", "Tipo", "Animal", "Peso"]
    conteudo = [
        ["2025-03-01", "Compra", "Boi 1", "450kg"],
        ["2025-03-10", "Venda", "Boi 2", "500kg"],
        ["2025-03-15", "Transferência", "Boi 3", "470kg"],
    ]
    return colunas, conteudo

def gerar_relatorio_compras_insumos():
    colunas = ["Data", "Insumo", "Quantidade", "Valor"]
    conteudo = [
        ["2025-02-20", "Ração", "300kg", "R$ 1.200,00"],
        ["2025-03-05", "Sal mineral", "50kg", "R$ 300,00"],
    ]
    return colunas, conteudo

def gerar_relatorio_consumo_insumos():
    colunas = ["Data", "Insumo", "Quantidade", "Finalidade"]
    conteudo = [
        ["2025-03-06", "Ração", "100kg", "Engorda"],
        ["2025-03-09", "Sal mineral", "20kg", "Suplementação"],
    ]
    return colunas, conteudo

def gerar_relatorio_vendas():
    colunas = ["Data", "Animal", "Peso", "Valor"]
    conteudo = [
        ["2025-03-10", "Boi 2", "500kg", "R$ 6.500,00"],
    ]
    return colunas, conteudo

def gerar_relatorio_balanco():
    colunas = ["Descrição", "Valor"]
    conteudo = [
        ["Vendas de Animais", "R$ 6.500,00"],
        ["Compras de Insumos", "- R$ 1.500,00"],
        ["Lucro Líquido", "R$ 5.000,00"],
    ]
    return colunas, conteudo
