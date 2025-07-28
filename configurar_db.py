def tabelas(id_user=1):
    TABELAS = {
        'users': """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password_hash TEXT
            );""",

        'localizacao': f"""CREATE TABLE IF NOT EXISTS localizacao_{id_user} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            endereco TEXT,
            coordenadas INTEGER
            );""",
        'lotes': f"""CREATE TABLE IF NOT EXISTS lotes_{id_user} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            quantidade INTEGER,
            localizacao INTEGER,
            descricao TEXT,
            FOREIGN KEY (localizacao) REFERENCES localizacao(id)
            );""",
        'racas': f"""CREATE TABLE IF NOT EXISTS racas_{id_user} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            descricao TEXT
            );""",
        'fornecedores': f"""CREATE TABLE IF NOT EXISTS fornecedores_{id_user} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            telefone TEXT,
            email TEXT
            );""",
        'clientes': f"""CREATE TABLE IF NOT EXISTS clientes_{id_user} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            email TEXT,
            telefone TEXT
            );""",
        'insumos': f"""CREATE TABLE IF NOT EXISTS insumos_{id_user} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            quantidade INTEGER,
            unidade TEXT,
            fornecedor_id INTEGER,
            FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id)
            );""",
        'animais_ativos': f"""CREATE TABLE IF NOT EXISTS animais_ativos_{id_user} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lote TEXT,
            raca INTEGER,
            data_nascimento INTEGER,
            fornecedor INTEGER,
            data_entrada INTEGER,
            peso_entrada INTEGER,
            valor_entrada INTEGER,
            consumo INTEGER
            );""",
        'animais_saida': f"""CREATE TABLE IF NOT EXISTS animais_saida_{id_user} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idx_entrada INTEGER,
            lote TEXT,
            raca INTEGER,
            data_nascimento INTEGER,
            fornecedor INTEGER,
            data_entrada INTEGER,
            peso_entrada INTEGER,
            valor_entrada INTEGER,
            consumo INTEGER,

            cliente TEXT,
            data_saida TEXT,
            peso_saida INTEGER,
            valor_saida INTEGER
        );""",
        'insumo_novo': f""" CREATE TABLE IF NOT EXISTS insumo_novo_{id_user} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            fornecedor TEXT,
            tipo TEXT,
            estoque TEXT,
            unidade TEXT
        );""",
        'insumo_compra': f""" CREATE TABLE IF NOT EXISTS insumo_compra_{id_user} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            insumo TEXT,
            data TEXT,
            quantidade TEXT,
            valor_unitario TEXT
        );""",
        'insumo_consumo': f""" CREATE TABLE IF NOT EXISTS insumo_consumo_{id_user} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            insumo TEXT,
            lote TEXT,
            data_inicio TEXT,
            data_fim TEXT,
            quantidade TEXT,
            observacao TEXT
        );"""
    }
    return TABELAS
