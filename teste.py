import requests
import json
import os
import time

# Carrega o histórico de perguntas e respostas
def carregar_historico():
    caminho = 'data/chat_historico.json'
    if not os.path.exists(caminho):
        os.makedirs('data', exist_ok=True)
        with open(caminho, 'w') as f:
            json.dump([
                {"role": "system", "content": "Responda sempre SOMENTE em português do Brasil, de forma precisa e detalhada.Você está analisando dados reais."}
            ], f)
        return [
            {"role": "system", "content": "Responda sempre SOMENTE em português do Brasil, de forma precisa e detalhada. Você está analisando dados reais."}
        ]
    with open(caminho, 'r') as f:
        return json.load(f)

def salvar_historico(historico):
    caminho = 'data/chat_historico.json'
    with open(caminho, 'w') as f:
        json.dump(historico, f, ensure_ascii=False, indent=4)

def aguardar_ollama_pronto(timeout=30):
    """Aguarda o Ollama estar disponível na porta 11434."""
    inicio = time.time()
    while time.time() - inicio < timeout:
        try:
            r = requests.get("http://localhost:11434")
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(1)
    raise TimeoutError("Ollama não respondeu dentro do tempo esperado.")

def perguntar_api(pergunta, historico):
    url = 'http://127.0.0.1:11434/api/chat'
    historico.append({"role": "user", "content": pergunta})
    payload = {
        "model": "llama3",
        "messages": historico,
        "stream": False,
        "max_tokens": 512,
        "temperature": 0.2
    }
    try:
        response = requests.post(url, json=payload, timeout=60)
        if response.status_code == 200:
            data = response.json()
            resposta = data.get("message", {}).get("content", "")
            historico.append({"role": "assistant", "content": resposta})
            return resposta
        else:
            print(f"\nErro: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print("Ollama não está rodando. Por favor, inicie o servidor Ollama manualmente.")
        return None
    except Exception as e:
        print(f"Erro ao acessar a API: {e}")
        return None

def main():
    print('Para sair digite "sair"')
    print('Aguardando Ollama iniciar...')
    try:
        aguardar_ollama_pronto()
    except Exception as e:
        print(f"Erro ao conectar ao Ollama: {e}")
        return

    historico = carregar_historico()
    while True:
        pergunta = input('>>> ')
        if pergunta.lower() == 'sair':
            print('Saindo...')
            salvar_historico(historico)
            break
        resposta = perguntar_api(pergunta, historico)
        if resposta:
            print(f'Resposta: {resposta}')
        else:
            print('Não foi possível obter resposta.')

if __name__ == "__main__":
    main()
