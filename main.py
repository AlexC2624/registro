import threading
import webbrowser
from app.init import app

PORT = 5000

def main():
    print('Iniciando o servidor...')
    # threading.Timer(3.0, lambda: webbrowser.open_new(f"http://127.0.0.1:{str(PORT)}")).start()
    app.run(port=PORT, debug=True)


if __name__ == '__main__': main()
