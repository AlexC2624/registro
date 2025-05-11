import threading
import webbrowser
from init import app

PORT = 5000

def main():
    """
    Função principal responsável por iniciar o servidor Flask. Ao ser executada, imprime uma mensagem
    indicando o início do servidor, aguarda 3 segundos e, em seguida, abre automaticamente o navegador
    padrão do usuário na URL correspondente ao servidor local.

    A aplicação Flask é iniciada na porta definida pela variável PORT com o modo de depuração ativado.

    Comportamento:
        - Exibe a mensagem "Iniciando o servidor..."
        - Aguarda 3 segundos e abre o navegador em http://127.0.0.1:<PORT>
        - Inicia o servidor Flask com debug=True

    Requisitos:
        - A variável global PORT deve estar definida com o número da porta desejada.
        - As bibliotecas threading e webbrowser devem estar importadas.
    """
    print('Iniciando o servidor...')
    # threading.Timer(3.0, lambda: webbrowser.open_new(f"http://127.0.0.1:{str(PORT)}")).start()
    app.run(port=PORT, debug=True)

if __name__ == '__main__': main()
