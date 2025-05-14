# from models import ManagerJSON
from  models import ManagerCSV

# m = ManagerJSON('data/json/animais.json')
# novoID = m.atualizar_dado('lote', {'nome': 'loteA'})

# print(m.formatar_dados('lote'))

# print(m.deletar_dado('lote', (int(novoID) - 1)))

csv = ManagerCSV('animal_entrada.csv')
csv_ler = csv.ler()
print(type(csv_ler))
print(csv_ler.columns)
print(list(csv_ler.columns))
print(csv_ler.shape)    # linha, coluna
print(csv_ler.index)
print(csv_ler.loc[0])
print(csv_ler.iloc[0])
print(csv_ler.values)
