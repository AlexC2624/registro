import threading
import webbrowser
from init import app
import socket

host, PORT = '0.0.0.0', 5000

def ip_atual():
    socket_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        socket_UDP.connect(('8.8.8.8', 80))
        ip = socket_UDP.getsockname()[0]
    except Exception: ip = '127.0.0.1'
    finally: socket_UDP.close()
    return ip
local_ip = ip_atual()

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
    print(f"Rota de início http://{local_ip}:{str(PORT)}/")
    print(f"Pata testes http://{local_ip}:{str(PORT)}/apidocs/")
    # threading.Timer(3.0, lambda: webbrowser.open_new(f"http://{local_ip}:{str(PORT)}")).start()
    app.run(host=host, port=PORT, debug=True)

if __name__ == '__main__': main()
