import sqlite3
import time
import os
from log import LOG

# --- Configurações ---
DB_FILE = 'data/dados.db'  # Nome do arquivo do seu banco de dados SQLite
SQL_SCRIPT_FILE = 'data/script.sql' # Nome do arquivo SQL a ser monitorado
MONITOR_INTERVAL_SECONDS = 2 # Intervalo de verificação em segundos

# --- Função para executar o script SQL e retornar dados ---
def execute_sql_script(db_path, sql_script_path):
    conn = None
    results = [] # Lista para armazenar os resultados de SELECTs e PRAGMAs
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        conn.set_trace_callback(lambda comando_sql: LOG().create_log(f'SQL Executado: {comando_sql}'))

        # print(f"Executando comandos do script '{sql_script_path}'...") # Mensagem adicionada para depuração

        with open(sql_script_path, 'r', encoding='utf-8') as f:
            # Lemos o script inteiro e o dividimos em comandos.
            # Uma regex simples pode ajudar a dividir melhor, mas para '; ' deve funcionar na maioria dos casos.
            sql_content = f.read()
            # Divide os comandos usando ';' como delimitador, e remove linhas vazias.
            # Isso é uma forma básica, mas funcional para scripts simples.
            statements = [s.strip() for s in sql_content.split(';')]

        for statement in statements:
            if not statement or '--' in statement or '/*' in statement or '*/' in statement:
                continue # Pula comandos vazios
            print(f"Executando comando: {statement}...") # Mensagem para depuração

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
            exit(1)  # Sai com erro se o arquivo não for encontrado
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
        # Se o arquivo SQL não existir, cria um exemplo básico
        with open(SQL_SCRIPT_FILE, 'w', encoding='utf-8') as f:
            f.write("""-- 1. Comando: CREATE TABLE
-- Cria uma tabela 'clientes' se ela ainda não existir.
-- Usamos IF NOT EXISTS para evitar erros se a tabela já existir.;
-- CREATE TABLE IF NOT EXISTS clientes (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     nome TEXT NOT NULL,
--     email TEXT UNIQUE,
--     data_cadastro TEXT DEFAULT CURRENT_TIMESTAMP
-- );

-- Cria uma tabela 'pedidos' se ela ainda não existir, com uma chave estrangeira para 'clientes'.;
-- CREATE TABLE IF NOT EXISTS pedidos (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     cliente_id INTEGER NOT NULL,
--     produto TEXT NOT NULL,
--     valor REAL NOT NULL,
--     data_pedido TEXT DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (cliente_id) REFERENCES clientes(id)
-- );

-- 2. Comando: INSERT INTO
-- Insere novos registros na tabela 'clientes'.;
-- INSERT INTO clientes (nome, email) VALUES ('Alice Silva', 'alice@example.com');
-- INSERT INTO clientes (nome, email) VALUES ('Bruno Costa', 'bruno@example.com');
-- INSERT INTO clientes (nome, email) VALUES ('Carla Dias', 'carla@example.com');

-- Insere novos registros na tabela 'pedidos'.
-- Certifique-se de que os 'cliente_id' existam na tabela 'clientes'.;
-- INSERT INTO pedidos (cliente_id, produto, valor) VALUES (1, 'Smartphone X', 1500.00);
-- INSERT INTO pedidos (cliente_id, produto, valor) VALUES (1, 'Capa de Smartphone', 50.00);
-- INSERT INTO pedidos (cliente_id, produto, valor) VALUES (2, 'Fone de Ouvido', 200.00);
-- INSERT INTO pedidos (cliente_id, produto, valor) VALUES (3, 'Smart TV 50"', 3000.00);

-- 3. Comando: SELECT
-- Seleciona todos os clientes da tabela 'clientes'.;
-- SELECT * FROM clientes;

-- Seleciona clientes com um nome específico.;
-- SELECT id, nome, email FROM clientes WHERE nome = 'Alice Silva';

-- Seleciona pedidos com valor maior que 1000.;
-- SELECT produto, valor FROM pedidos WHERE valor > 1000;

-- 4. Comando: UPDATE
-- Atualiza o email de um cliente.;
-- UPDATE clientes SET email = 'alice.silva@newemail.com' WHERE nome = 'Alice Silva';

-- Atualiza o valor de um produto específico.;
-- UPDATE pedidos SET valor = 250.00 WHERE produto = 'Fone de Ouvido';

-- 5. Comando: SELECT com JOIN
-- Seleciona informações combinadas das tabelas 'clientes' e 'pedidos'.;
-- SELECT
--     c.nome AS NomeCliente,
--     p.produto AS ProdutoComprado,
--     p.valor AS ValorPedido
-- FROM
--     clientes c
-- JOIN
--     pedidos p ON c.id = p.cliente_id
-- WHERE
--     p.valor > 100;

-- 6. Exemplo de "SELECT INTO" no SQLite (via CREATE TABLE AS SELECT)
-- SQLite não tem um comando SELECT INTO direto para criar e popular uma tabela em uma única instrução
-- como SQL Server. A abordagem equivalente é usar CREATE TABLE AS SELECT.
-- Isso cria uma nova tabela 'clientes_vip' com dados selecionados da tabela 'clientes'.;
-- CREATE TABLE IF NOT EXISTS clientes_vip AS
-- SELECT id, nome, email
-- FROM clientes
-- WHERE nome LIKE 'Alice%';

-- Seleciona dados da nova tabela 'clientes_vip'.;
-- SELECT * FROM clientes_vip;

-- 7. Comando: DELETE
-- Deleta um registro específico da tabela 'pedidos'.
-- Cuidado ao usar DELETE sem WHERE, pois ele remove todas as linhas da tabela!;
-- DELETE FROM pedidos WHERE produto = 'Capa de Smartphone';

-- Deleta um cliente pelo nome (e quaisquer pedidos relacionados se configurado com CASCADE no FOREIGN KEY,
-- ou você precisaria deletar os pedidos primeiro).;
-- DELETE FROM clientes WHERE nome = 'Bruno Costa';

-- 8. Comando: DROP TABLE (Cuidado! Isso remove a tabela e todos os seus dados)
-- Usado geralmente para limpar o ambiente de teste.;
-- DROP TABLE IF EXISTS insumo_compra_1;
-- DROP TABLE IF EXISTS animais_saldo_1;
-- DROP TABLE IF EXISTS clientes_vip;

-- 9. Comando: Listar todas as tabelas no banco de dados
-- Consulta a tabela mestra 'sqlite_master' que armazena informações sobre o schema.;
-- SELECT name FROM sqlite_master WHERE type='table';

-- 10. Comando: Listar colunas de uma tabela específica (Ex: 'clientes')
-- O comando PRAGMA table_info(nome_da_tabela) retorna detalhes das colunas.;
-- PRAGMA table_info('clientes_1');

-- 11. Comando: Listar colunas de outra tabela específica (Ex: 'pedidos');
-- PRAGMA table_info(pedidos);

-- 12. Comando: Listar colunas da tabela 'clientes_vip' (se ela foi criada);
-- PRAGMA table_info(clientes_vip);
""")
        print(f"Erro: O arquivo SQL '{SQL_SCRIPT_FILE}' não foi encontrado. Mas ele foi criado com alguns exemplos, edite como precisa e tente novamente.")

    else:
        try: monitor_and_execute(DB_FILE, SQL_SCRIPT_FILE, MONITOR_INTERVAL_SECONDS)
        except KeyboardInterrupt:
            print("\nMonitoramento interrompido.")
