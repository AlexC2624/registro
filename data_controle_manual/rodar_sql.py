import sqlite3
import time
import os

# --- Configurações ---
DB_FILE = 'data/dados.db'  # Nome do arquivo do seu banco de dados SQLite
SQL_SCRIPT_FILE = 'data_controle_manual/script.sql' # Nome do arquivo SQL a ser monitorado
MONITOR_INTERVAL_SECONDS = 2 # Intervalo de verificação em segundos

# --- Função para executar o script SQL ---
def execute_sql_script(db_path, sql_script_path):
    conn = None # Inicializa a conexão como None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print(f"\n--- Executando '{sql_script_path}' em '{db_path}' ---")

        with open(sql_script_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        # executescript() é ótimo para múltiplos comandos SQL separados por ';'
        cursor.executescript(sql_script)
        conn.commit()
        print(f"Script '{sql_script_path}' executado com sucesso!")

        # Opcional: Mostrar alguns dados depois da execução
        cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC LIMIT 3")
        print("Últimos logs no banco de dados:")
        for row in cursor.fetchall():
            print(f"- {row}")

    except FileNotFoundError:
        print(f"ERRO: Arquivo SQL '{sql_script_path}' não encontrado.")
    except sqlite3.Error as e:
        print(f"ERRO ao executar script SQL no SQLite: {e}")
    finally:
        if conn:
            conn.close()
            print("Conexão com o banco de dados fechada.")

# --- Lógica de Monitoramento ---
def monitor_and_execute(db_file, sql_file, interval):
    last_modified_time = None
    print(f"Monitorando o arquivo '{sql_file}' a cada {interval} segundos...")
    print("Pressione Ctrl+C para sair.")

    while True:
        try:
            # Pega a data e hora da última modificação do arquivo
            current_modified_time = os.path.getmtime(sql_file)

            if last_modified_time is None or current_modified_time > last_modified_time:
                print(f"Mudança detectada em '{sql_file}' às {time.ctime(current_modified_time)}")
                execute_sql_script(db_file, sql_file)
                last_modified_time = current_modified_time

        except FileNotFoundError:
            print(f"AVISO: Arquivo SQL '{sql_file}' não encontrado. Verifique o caminho.")
        except KeyboardInterrupt:
            print("\nMonitoramento interrompido pelo usuário.")
            break
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

        time.sleep(interval)

# --- Execução Principal ---
if __name__ == "__main__":
    # Garante que o arquivo SQL exista antes de iniciar o monitoramento
    if not os.path.exists(SQL_SCRIPT_FILE):
        print(f"Erro: O arquivo SQL '{SQL_SCRIPT_FILE}' não foi encontrado. Por favor, crie-o.")
    else:
        # Inicia o monitoramento
        monitor_and_execute(DB_FILE, SQL_SCRIPT_FILE, MONITOR_INTERVAL_SECONDS)