import pandas as pd
import requests

# Qantos animais foran comprados?

# Pré-carrega os arquivos
arquivos = {
    "compras_animais": pd.read_csv("data/animal_entrada.csv"),
    # "vendas_animais": pd.read_csv("dados/animal_vendido.csv"),
    # "insumos_comprados": pd.read_csv("dados/insumo_comprado.csv"),
    # "insumos_consumidos": pd.read_csv("dados/insumo_consumo.csv"),
}

def interpretar_pergunta(pergunta: str):
    if "compra" in pergunta.lower():
        df = arquivos["compras_animais"]
        dados = df.tail(50).to_string(index=False)  # ou aplicar filtro com base em datas
    # elif "compra" in pergunta.lower() and "animal" in pergunta.lower():
    #     df = arquivos["compras_animais"]
    #     dados = df.tail(50).to_string(index=False)
    # elif "insumo" in pergunta.lower() and "consumido" in pergunta.lower():
    #     df = arquivos["insumos_consumidos"]
    #     dados = df.tail(50).to_string(index=False)
    else:
        dados = "Desculpe, não consegui identificar os dados corretos para essa pergunta."
    return dados

def perguntar_ao_modelo(dados, pergunta):
    mensagens = [
        {"role": "system", "content": "Você é um assistente que responde com base apenas nos dados fornecidos."},
        {"role": "user", "content": f"{dados}\n\nAgora responda à pergunta:\n{pergunta}"}
    ]
    r = requests.post("http://localhost:11434/api/chat", json={
        "model": "llama3",
        "messages": mensagens,
        "stream": False
    })
    try: return r.json()["message"]["content"]
    except KeyError: return r.json()['error']

# Loop principal
while True:
    pergunta = input("\nDigite sua pergunta ou 'sair': ")
    if pergunta.lower() == "sair":
        break
    dados_relevantes = interpretar_pergunta(pergunta)
    resposta = perguntar_ao_modelo(dados_relevantes, pergunta)
    print(f"\nResposta da IA:\n{resposta}")
