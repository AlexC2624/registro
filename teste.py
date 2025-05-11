from models import ManagerJSON

m = ManagerJSON('data/json/animais.json')
# novoID = m.atualizar_dado('lote', {'nome': 'loteA'})

print(m.formatar_dados('lote'))

# print(m.deletar_dado('lote', (int(novoID) - 1)))