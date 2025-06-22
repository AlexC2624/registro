import ollama
import json

class OllamaChatbot:
    """
    Uma classe para instanciar e gerenciar a interação com um modelo Ollama local.
    Permite configurar o modelo, opções de inferência e manter um histórico de conversa.
    """

    def __init__(self, model_name: str = 'llama2', system_message: str = 'Você é um assistente prestativo. Responda de forma concisa e útil.', max_history_size: int = 10, **inference_options):
        """
        Inicializa o chatbot Ollama.

        Args:
            model_name (str): O nome do modelo Ollama a ser usado (ex: 'llama2', 'mistral').
            system_message (str): Uma mensagem inicial do sistema para guiar o comportamento da IA.
            max_history_size (int): O número máximo de mensagens (usuário + IA) para manter no histórico.
                                    A mensagem do sistema não conta para este limite.
            **inference_options: Opções adicionais para a inferência do modelo,
                                 como 'temperature', 'top_k', 'top_p', 'num_ctx', etc.
        """
        self.model_name = model_name
        self.max_history_size = max_history_size

        # Configura as opções de inferência, usando valores padrão se não fornecidos
        self.inference_options = {
            "temperature": 0.7,
            "top_k": 40,
            "top_p": 0.9,
            "num_ctx": 2048, # O tamanho da janela de contexto padrão do modelo
            **inference_options # Sobrescreve as padrões com as fornecidas
        }

        # Inicializa o histórico de conversa com a mensagem do sistema
        self.history = [{'role': 'system', 'content': system_message}]

        print(f"Chatbot Ollama inicializado com o modelo: {self.model_name}")
        print(f"Opções de inferência: {self.inference_options}")

    def ask(self, user_question: str) -> str:
        """
        Envia uma pergunta ao modelo Ollama e retorna a resposta.
        Gerencia o histórico de conversa para manter a 'memória'.

        Args:
            user_question (str): A pergunta do usuário.

        Returns:
            str: A resposta gerada pelo modelo Ollama.
        """
        # Adiciona a pergunta do usuário ao histórico
        self.history.append({'role': 'user', 'content': user_question})

        # Garante que o histórico não exceda o tamanho máximo definido,
        # mantendo sempre a mensagem do sistema e as últimas interações.
        # (- self.max_history_size * 2) é uma heurística para pares de conversas (usuário+IA)
        # Ajustamos para pegar o suficiente para o limite + a mensagem do sistema.
        if len(self.history) > self.max_history_size + 1: # +1 para a mensagem do sistema
            self.history = [self.history[0]] + self.history[-(self.max_history_size * 2):]
            # O *2 é porque cada pergunta e resposta conta como 2 entradas (user e assistant)
            # Se o max_history_size for 10, queremos manter 10 pares de conversa + a mensagem do sistema.
            # Então, vamos manter as últimas 20 mensagens (10 de user, 10 de assistant)
            # Mais a mensagem do sistema no início.

        try:
            print(f"\n[Enviando pergunta para Ollama ({self.model_name})...]")
            response = ollama.chat(
                model=self.model_name,
                messages=self.history,
                options=self.inference_options
            )

            ai_response = response['message']['content']

            # Adiciona a resposta da IA ao histórico
            self.history.append({'role': 'assistant', 'content': ai_response})

            return ai_response

        except ollama.ResponseError as e:
            print(f"Erro de resposta do Ollama: {e}")
            return f"Desculpe, ocorreu um erro ao obter a resposta do modelo: {e}"
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            print("Verifique se o servidor Ollama está rodando e se o modelo está baixado.")
            print(f"Comando para verificar: 'ollama list'")
            print(f"Comando para puxar modelo: 'ollama pull {self.model_name}'")
            return "Desculpe, ocorreu um erro inesperado na comunicação."

    def get_history(self) -> list:
        """Retorna o histórico de conversa atual."""
        return self.history

    def clear_history(self):
        """Limpa o histórico de conversa, mantendo apenas a mensagem do sistema."""
        self.history = [self.history[0]]
        print("Histórico de conversa limpo.")


# --- Exemplo de Uso da Classe ---
if __name__ == "__main__":
    # 1. Crie uma instância do seu chatbot
    # Você pode personalizar o modelo, a mensagem do sistema e as opções de inferência
    my_chatbot = OllamaChatbot(
        model_name='gemma3:1b', # Altere para o modelo que você tem baixado
        system_message='Você é um assistente especialista em gado de corte e agronegócio. Responda de forma detalhada e técnica.',
        max_history_size=10, # Manter até 10 pares de perguntas/respostas no histórico
        temperature=0.6,     # Um pouco menos criativo
        num_ctx=4096         # Aumentar a janela de contexto se o modelo suportar
    )

    print("\n--- Início da Conversa com o Chatbot ---")
    print("Digite 'sair' para encerrar.")
    print("Digite 'limpar' para limpar o histórico da conversa.")

    while True:
        user_input = input("\nVocê: ")

        if user_input.lower() == 'sair':
            print("Encerrando o chatbot. Até logo!")
            break
        elif user_input.lower() == 'limpar':
            my_chatbot.clear_history()
            continue # Pula para a próxima iteração do loop

        response_from_ai = my_chatbot.ask(user_input)
        print(f"IA: {response_from_ai}")

        # Opcional: ver o histórico completo para depuração
        # print("\n--- Histórico de Conversa Atual ---")
        # for msg in my_chatbot.get_history():
        #     print(f"  {msg['role'].capitalize()}: {msg['content'][:70]}...") # Limita para não poluir
        # print("----------------------------------")