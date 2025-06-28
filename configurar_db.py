def tabelas(id_user=1):
    TABELAS = {
        'CREATE_TABLE_USER': """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password_hash TEXT
            );""",

        'CREATE_TABLE_LOCALIZACAO': f"""CREATE TABLE IF NOT EXISTS localizacao_{id_user} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            endereco TEXT,
            coordenadas INTEGER
            );""",
        'CREATE_TABLE_LOTE': f"""CREATE TABLE IF NOT EXISTS lotes_{id_user} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            quantidade INTEGER,
            localizacao INTEGER,
            descricao TEXT,
            FOREIGN KEY (localizacao) REFERENCES localizacao(id)
            );""",
        'CREATE_TABLE_RACA': f"""CREATE TABLE IF NOT EXISTS racas_{id_user} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            descricao TEXT
            );""",
        'CREATE_TABLE_FORNECEDOR': f"""CREATE TABLE IF NOT EXISTS fornecedores_{id_user} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            telefone TEXT,
            email TEXT
            );""",
        'CREATE_TABLE_CLIENTE': f"""CREATE TABLE IF NOT EXISTS clientes_{id_user} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            email TEXT,
            telefone TEXT
            );""",
        'CREATE_TABLE_INSUMO': f"""CREATE TABLE IF NOT EXISTS insumos_{id_user} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            quantidade INTEGER,
            unidade TEXT,
            fornecedor_id INTEGER,
            FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id)
            );""",
        'CREATE_TABLE_ANIMAIS_ENTRADA': f"""CREATE TABLE IF NOT EXISTS animais_entrada_{id_user} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lote TEXT,
            raca INTEGER,
            data_nascimento INTEGER,
            fornecedor INTEGER,
            data_entrada INTEGER,
            peso_entrada INTEGER,
            valor_entrada INTEGER
            );""",
        'CREATE_TABLE_ANIMAIS_SAIDA': f"""CREATE TABLE IF NOT EXISTS animais_saida_{id_user} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            idade INTEGER,
            peso INTEGER,
            raca_id INTEGER,
            lote_id INTEGER,
            cliente_id INTEGER,
            FOREIGN KEY (raca_id) REFERENCES racas(id),
            FOREIGN KEY (lote_id) REFERENCES lotes(id),
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        );"""
    }
    return TABELAS
