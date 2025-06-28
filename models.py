import sqlite3  # Importa o módulo sqlite3 para manipulação de banco de dados SQLite
import re   # Importa o módulo re para expressões regulares

class SQL:

    # Colunas não permitidas para cada tabela
    _DISALLOWED_COLUMNS = {
        'clientes': {'id'},
        'pedidos': {'id', 'cliente_id'},
        'produtos': {'id', 'preco'},
    }

    def __init__(self, sql_creat:dict, nome_db:str='dados.db'):
        """
        Inicializa uma nova instância da classe, conectando ao banco de dados SQLite especificado e configurando o cursor.
        Ativa o modo de depuração para exibir consultas SQL executadas.
        Args:
            sql_creat (dict): Dicionário contendo os comandos SQL para criação das tabelas. ATENÇÃO, a chave deve ser igual ao nome fixo da tabela.
            nome_db (str, opcional): Nome do arquivo do banco de dados SQLite. Padrão é 'dados.db'.
        """

        self.conn = sqlite3.connect(nome_db)
        self.cursor = self.conn.cursor()
        self.conn.set_trace_callback(print)  # Ativa o modo de depuração para exibir consultas SQL
        self.sql_creat = sql_creat

    def criar_tabela(self, string_sql):
        """
        Cria uma tabela no banco de dados com base na string SQL fornecida.
        
        Args:
            string_sql (str): Comando SQL para criar a tabela ou a chave do dict informado na instância.
        """
        if string_sql in self.sql_creat.keys(): string_sql = self.sql_creat[string_sql]
        self.cursor.execute(string_sql)
        self.conn.commit()

    def inserir(self, tabela='users', colunas=['nome', 'email', 'telefone'], valores=['Ana', 'ana@mail.com', 123456789]):
        """Insere um registro na tabela com base nas colunas e nos valores fornecidos.
        Args:
            colunas (list of str): Lista com os nomes cas colunas.
            valores (tuple): Valores a serem inseridos na tabela.
        """
        string_sql = f"INSERT INTO {tabela} ({', '.join(colunas)}) VALUES ({', '.join(['?' for _ in colunas])});"
        valores = tuple(valores)
        try:
            self.cursor.execute(string_sql, valores)
        except sqlite3.OperationalError as e:
            self.criar_tabela(tabela)
            self.cursor.execute(string_sql, valores)

        self.conn.commit()
        return True, f'Cadastro em {tabela} realizad com sucesso'

    def ler_tabela(self, nome_tabela='tabela', colunas=['*']):
        """
        Lê dados de uma tabela específica no banco de dados. Se não encontrar a tabela tenta criá-la somente uma vez.

        Args:
            nome_tabela (str): Nome da tabela a ser lida. Padrão é 'tabela'.
            colunas (list of str): Lista com os nomes das colunas a serem selecionadas. Padrão é ['*'] (todas as colunas).

        Returns:
            list: Lista de tuplas contendo os registros encontrados na tabela.
        """
        string_sql = f'SELECT {', '.join(colunas)} FROM {nome_tabela}'
        try:
            self.cursor.execute(string_sql)
        except sqlite3.OperationalError as e:
            self.criar_tabela(nome_tabela)
            self.cursor.execute(string_sql)
        return self.cursor.fetchall()

    def buscar_registro(self, tabela:str, coluna:str, valor:str) -> list:
        """        Busca registros em uma tabela específica onde uma coluna tem um valor específico.
        Args:
            tabela (str): Nome da tabela onde a busca será realizada.
            coluna (str): Nome da coluna onde o valor será buscado.
            valor (str): Valor a ser buscado na coluna especificada.
        Returns:
            list: Lista de tuplas contendo os registros encontrados. Retorna uma lista vazia se nenhum registro for encontrado.
        """
        string_sql = f"SELECT * FROM {tabela} WHERE {coluna} = ?"
        try: self.cursor.execute(string_sql, (valor,))
        except sqlite3.OperationalError as e:
            self.criar_tabela(tabela)
            self.cursor.execute(string_sql, (valor,))

        return self.cursor.fetchall()

    def consulta_sql(self, sql_query: str, params: tuple = None) -> list | None:
        """
        Executa uma query SQL de leitura (SELECT) de forma segura no banco de dados.

        Este método garante que apenas operações de leitura sejam realizadas e utiliza
        parametrização para prevenir ataques de SQL Injection.

        Args:
            sql_query (str): A string da query SQL a ser executada. Deve ser uma
                             instrução SELECT. Para parâmetros, use '?' como placeholder.
                             Ex: "SELECT nome, idade FROM usuarios WHERE id = ?"
            params (tuple, optional): Uma tupla de valores para substituir os placeholders
                                      na `sql_query`. Deve ser fornecida na ordem dos
                                      placeholders. Padrão para None se não houver parâmetros.

        Returns:
            list: Uma lista de tuplas, onde cada tupla representa uma linha do resultado
                  da consulta. Retorna uma lista vazia se a consulta não encontrar resultados.
            str: Uma mensagem de erro caso a query não seja SELECT ou ocorra uma exceção.
        """
        try:
            # 1. Verifica se a query é uma operação de leitura
            sql_upper = sql_query.strip().upper()
            if not sql_upper.startswith("SELECT"):
                return "Erro: A função 'executar_sql' permite apenas queries SELECT."

            # 2. Extrai o nome da tabela (simplificado, assume FROM direto após SELECT/colunas)
            # Isso é uma simplificação. Para SQL mais complexo, um parser real seria necessário.
            match_from = re.search(r"FROM\s+([a-zA-Z0-9_]+)", sql_upper)
            if not match_from:
                return "Erro: Não foi possível identificar a tabela na query SQL."
            table_name = match_from.group(1).lower()

            # 3. Obtém as colunas permitidas do dicionário estático
            allowed_columns_for_table = self._DISALLOWED_COLUMNS.get(table_name)
            if allowed_columns_for_table:
                return f"Erro: Acesso não permitido ou tabela '{table_name}' não configurada para acesso."

            # 3. Extrai as colunas da cláusula SELECT
            # Encontra a parte entre SELECT e FROM (ou WHERE, JOIN, etc.)
            select_part_match = re.search(r"SELECT\s+(.*?)\s+FROM", sql_upper, re.DOTALL)
            if not select_part_match:
                # Caso de SELECT * sem FROM ou FROM em outra linha, mais complexo
                return "Erro: Formato de SELECT inválido. Não foi possível extrair colunas."

            selected_columns_str = select_part_match.group(1).strip()

            selected_columns = set()
            if selected_columns_str == "*":
                # Se for SELECT *, consideramos todas as colunas da tabela como selecionadas
                selected_columns = allowed_columns_for_table
            else:
                # Divide por vírgulas, remove espaços e converte para minúsculas
                raw_cols = selected_columns_str.split(',')
                for col in raw_cols:
                    clean_col = col.strip().lower()
                    # Remove alias se houver (ex: 'nome AS full_name')
                    if ' ' in clean_col:
                        clean_col = clean_col.split(' ')[0]
                    selected_columns.add(clean_col)

            # 4. Compara as colunas selecionadas com as colunas permitidas
            # Verifica se todas as colunas selecionadas estão contidas nas permitidas
            if not selected_columns.issubset(allowed_columns_for_table):
                # Identifica quais colunas são indevidas
                forbidden_columns = selected_columns - allowed_columns_for_table
                return (f"Erro: Tentativa de acessar colunas indevidas: "
                        f"{', '.join(forbidden_columns)}. Apenas as seguintes colunas "
                        f"são permitidas para a tabela '{table_name}': "
                        f"{', '.join(allowed_columns_for_table)}.")

            # Se todas as verificações passarem, executa a query
            if params:
                self.cursor.execute(sql_query, params)
            else:
                self.cursor.execute(sql_query)

            return self.cursor.fetchall()

        except Exception as e:
            return f"Ocorreu um erro inesperado: {e}"

    def __exit__(self):
        """Fecha a conexão com o banco de dados ao sair do contexto."""
        if hasattr(self, 'conn'):
            self.conn.close()
            print("Conexão com o banco de dados fechada.")
        return False
