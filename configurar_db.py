def tabelas():
    TABELAS = {
        # Tabela 1: Cadastro de Usuários e Propriedades
        # Mantém informações básicas do usuário.
        'users': """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_usuario TEXT NOT NULL,
            senha_hash TEXT NOT NULL,
            email TEXT UNIQUE,
            telefone INTEGER,
            estado TEXT,
            cidade TEXT,
            comunidade TEXT
        );""",

        # Tabela 2: Cadastros Essenciais
        # Substitui a tabela 'outros' para maior organização e integridade dos dados.
        # Cada entidade tem sua própria tabela.
        'racas': """CREATE TABLE IF NOT EXISTS racas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER NOT NULL,
            nome TEXT NOT NULL UNIQUE,
            descricao TEXT,
            FOREIGN KEY(id_user) REFERENCES users(id)
        );""",

        'fornecedores_clientes': """CREATE TABLE IF NOT EXISTS fornecedores_clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER NOT NULL,
            nome TEXT NOT NULL,
            tipo TEXT CHECK(tipo IN ('fornecedor', 'cliente', 'ambos')) NOT NULL,
            telefone TEXT,
            email TEXT,
            FOREIGN KEY(id_user) REFERENCES users(id)
        );""",
        
        'lotes': """CREATE TABLE IF NOT EXISTS lotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER NOT NULL,
            nome TEXT NOT NULL UNIQUE,
            descricao TEXT,
            capacidade INTEGER,
            FOREIGN KEY(id_user) REFERENCES users(id)
        );""",
        
        'insumos': """CREATE TABLE IF NOT EXISTS insumos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER NOT NULL,
            nome TEXT NOT NULL UNIQUE,
            tipo TEXT CHECK(tipo IN ('raca', 'suplemento', 'medicamento', 'vacina', 'material')) NOT NULL,
            unidade_medida TEXT NOT NULL,
            FOREIGN KEY(id_user) REFERENCES users(id)
        );""",
        
        # Tabela 3: Dados Mestres dos Animais
        # Armazena informações permanentes sobre cada animal. Movimentações
        # (compra, venda, morte) e dados de produção/saúde ficam em outras tabelas.
        'animais': """CREATE TABLE IF NOT EXISTS animais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER NOT NULL,
            identificacao TEXT UNIQUE, -- Ex: brinco, nome
            raca_id INTEGER,
            sexo TEXT CHECK(sexo IN ('macho', 'femea')),
            data_nascimento TEXT,
            status TEXT CHECK(status IN ('ativo', 'vendido', 'morto')),
            FOREIGN KEY(raca_id) REFERENCES racas(id),
            FOREIGN KEY(id_user) REFERENCES users(id)
        );""",

        # Tabela 4: Movimentações do Rebanho
        # Registra todas as entradas e saídas de animais.
        'movimentacoes_animal': """CREATE TABLE IF NOT EXISTS movimentacoes_animal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER NOT NULL,
            animal_id INTEGER,
            tipo_movimentacao TEXT CHECK(tipo_movimentacao IN ('compra', 'venda', 'morte', 'transferencia')) NOT NULL,
            data TEXT NOT NULL,
            lote_id_atual INTEGER,
            peso_kg REAL,
            valor_unitario_brl REAL,
            fornecedor_cliente_id INTEGER,
            observacoes TEXT,
            FOREIGN KEY(animal_id) REFERENCES animais(id),
            FOREIGN KEY(lote_id_atual) REFERENCES lotes(id),
            FOREIGN KEY(fornecedor_cliente_id) REFERENCES fornecedores_clientes(id),
            FOREIGN KEY(id_user) REFERENCES users(id)
        );""",

        # Tabela 5: Gestão de Estoque e Consumo de Insumos
        # Registra todas as transações de insumos.
        'estoque': """CREATE TABLE IF NOT EXISTS estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER NOT NULL,
            insumo_id INTEGER,
            tipo_movimentacao TEXT CHECK(tipo_movimentacao IN ('entrada', 'consumo')) NOT NULL,
            data TEXT NOT NULL,
            quantidade REAL NOT NULL,
            valor_unitario_brl REAL,
            lote_id_destino INTEGER,
            observacoes TEXT,
            FOREIGN KEY(insumo_id) REFERENCES insumos(id),
            FOREIGN KEY(lote_id_destino) REFERENCES lotes(id),
            FOREIGN KEY(id_user) REFERENCES users(id)
        );""",

        # Tabela 6: Saúde e Produção do Rebanho
        # Registra medições e eventos de saúde para cada animal.
        'saude_producao': """CREATE TABLE IF NOT EXISTS saude_producao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER NOT NULL,
            animal_id INTEGER,
            tipo_evento TEXT CHECK(tipo_evento IN ('vacina', 'medicamento', 'pesagem', 'observacao')) NOT NULL,
            data TEXT NOT NULL,
            medicamento_id INTEGER, -- FK para insumos se for medicamento
            peso_kg REAL,
            comportamento TEXT,
            valor_servico_brl REAL,
            observacoes TEXT,
            FOREIGN KEY(animal_id) REFERENCES animais(id),
            FOREIGN KEY(medicamento_id) REFERENCES insumos(id),
            FOREIGN KEY(id_user) REFERENCES users(id)
        );"""
    }
    return TABELAS
