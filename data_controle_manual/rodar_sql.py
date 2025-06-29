import sqlite3
import time
import os
import logging

# --- Configurações ---
DB_FILE = 'data/dados.db'  # Nome do arquivo do seu banco de dados SQLite
SQL_SCRIPT_FILE = 'data_controle_manual/script.sql' # Nome do arquivo SQL a ser monitorado
MONITOR_INTERVAL_SECONDS = 2 # Intervalo de verificação em segundos

# --- Função para executar o script SQL e retornar dados ---
def execute_sql_script(db_path, sql_script_path):
    conn = None
    results = [] # Lista para armazenar os resultados de SELECTs e PRAGMAs
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 1. Configurar o logger no __init__
        logger = logging.getLogger(__name__)
        # Define o nível mínimo de log para este logger
        logger.setLevel(logging.DEBUG)

        # Cria um FileHandler para escrever no arquivo de log
        log_file_path = 'data/log_db.log'
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.DEBUG) # Nível mínimo para o arquivo de log

        # Cria um Formatter para definir o formato das mensagens
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Adiciona o handler ao logger, se ele ainda não foi adicionado
        # Isso previne a adição de múltiplos handlers em chamadas subsequentes do __init__
        if not logger.handlers:
            logger.addHandler(file_handler)
        
        conn.set_trace_callback(lambda comando_sql: logger.debug(f'SQL Executado: {comando_sql}'))

        print(f"Executando comandos do script '{sql_script_path}'...") # Mensagem adicionada para depuração

        with open(sql_script_path, 'r', encoding='utf-8') as f:
            # Lemos o script inteiro e o dividimos em comandos.
            # Uma regex simples pode ajudar a dividir melhor, mas para '; ' deve funcionar na maioria dos casos.
            sql_content = f.read()
            # Divide os comandos usando ';' como delimitador, e remove linhas vazias.
            # Isso é uma forma básica, mas funcional para scripts simples.
            statements = [s.strip() for s in sql_content.split(';') if s.strip()]

        for statement in statements:
            if not statement:
                continue # Pula comandos vazios

            try:
                # Tenta executar o comando
                cursor.execute(statement)

                # Verifica se há resultados para buscar (para SELECTs e PRAGMAs)
                # sqlite3.cursor.description é None para comandos que não retornam linhas (DML/DDL)
                # e é uma tupla de descrições de coluna para comandos que retornam.
                if cursor.description:
                    columns = [description[0] for description in cursor.description]
                    rows = cursor.fetchall()
                    if rows:
                        results.append({"statement": statement, "columns": columns, "data": rows})
                else:
                    # Se não houver descrição, é um comando que altera o DB (INSERT, UPDATE, DELETE, CREATE, DROP)
                    # ou um PRAGMA que não retorna rows (raro, mas possível para alguns PRAGMAs de configuração)
                    conn.commit() # Confirma as alterações

            except sqlite3.Error as stmt_e:
                print(f"ERRO ao executar comando: '{statement[:70]}...': {stmt_e}")
                conn.rollback() # Desfaz em caso de erro

        print(f"Script '{sql_script_path}' executado. {len(results)} conjuntos de resultados encontrados.") # Mensagem para depuração

    except FileNotFoundError:
        print(f"ERRO: Arquivo SQL '{sql_script_path}' não encontrado.")
    except sqlite3.Error as e:
        print(f"ERRO geral ao conectar/executar no SQLite: {e}")
    finally:
        if conn:
            conn.close()
    return results

# --- Lógica de Monitoramento ---
def monitor_and_execute(db_file, sql_file, interval):
    last_modified_time = None
    print(f"Monitorando o arquivo '{sql_file}' a cada {interval} segundos... (Pressione Ctrl+C para sair)")

    while True:
        try:
            current_modified_time = os.path.getmtime(sql_file)

            if last_modified_time is None or current_modified_time > last_modified_time:
                print(f"\n--- Mudança detectada em '{sql_file}' às {time.ctime(current_modified_time)} ---")
                returned_data = execute_sql_script(db_file, sql_file)
                if returned_data:
                    print("--- Resultados de Comandos SELECT/PRAGMA ---")
                    for item in returned_data:
                        print(f"  Comando: {item['statement'][:70]}...")
                        print(f"  Colunas: {', '.join(item['columns'])}")
                        # Limita a exibição a, por exemplo, 5 primeiras linhas para não sobrecarregar o terminal
                        for i, row in enumerate(item['data']):
                            if i >= 15:
                                print(f"    ... e mais {len(item['data']) - 15} linhas.")
                                break
                            print(f"    {row}")
                        print("-" * 40) # Separador visual
                else:
                    print("Nenhum dado retornado de comandos SELECT/PRAGMA neste script.")
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
    # Garante que a pasta 'data' exista para o DB_FILE
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    # Garante que a pasta 'data_controle_manual' exista
    os.makedirs(os.path.dirname(SQL_SCRIPT_FILE), exist_ok=True)


    if not os.path.exists(SQL_SCRIPT_FILE):
        print(f"Erro: O arquivo SQL '{SQL_SCRIPT_FILE}' não foi encontrado. Por favor, crie-o.")
        print(f"Exemplo de conteúdo para '{SQL_SCRIPT_FILE}':")
        print("---")
        print("CREATE TABLE IF NOT EXISTS teste (id INTEGER PRIMARY KEY, nome TEXT);")
        print("INSERT INTO teste (nome) VALUES ('Item A');")
        print("INSERT INTO teste (nome) VALUES ('Item B');")
        print("SELECT * FROM teste;")
        print("SELECT name FROM sqlite_master WHERE type='table';")
        print("PRAGMA table_info(teste);")
        print("---")
    else:
        monitor_and_execute(DB_FILE, SQL_SCRIPT_FILE, MONITOR_INTERVAL_SECONDS)
