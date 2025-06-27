from models import SQL

def configurar_banco_dados(id_user:str):
    STRING_SQL = {
        'CREATE_TABLE_USER': f"""CREATE TABLE IF NOT EXISTS users_{id_user} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        );""",
        'CREATE_TABLE_LOCALIZACAO': f"""CREATE TABLE IF NOT EXISTS localizacao_{id_user} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            endereco TEXT NOT NULL,
            coordenadas INTEGER
        );""",

        'CREATE_TABLE_LOTE': f"""CREATE TABLE IF NOT EXISTS lote_{id_user} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            quantidade INTEGER NOT NULL,
            localizacao INTEGER NOT NULL,
            descricao TEXT,
            FOREIGN KEY (localizacao) REFERENCES localizacao(id)
        );""",

        'CREATE_TABLE_RACA': f"""CREATE TABLE IF NOT EXISTS racas_{id_user} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            descricao TEXT
        );""",

        'CREATE_TABLE_FORNECEDOR': f"""CREATE TABLE IF NOT EXISTS fornecedores_{id_user} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            telefone TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        );""",

        'CREATE_TABLE_CLIENTE': f"""CREATE TABLE IF NOT EXISTS clientes_{id_user} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            telefone TEXT
        );""",

        'CREATE_TABLE_INSUMO': f"""CREATE TABLE IF NOT EXISTS insumos_{id_user} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            quantidade INTEGER NOT NULL,
            unidade TEXT NOT NULL,
            fornecedor_id INTEGER,
            FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id)
        );"""
    }

    SQL('data/dados.db', STRING_SQL).conn.close()
