def tabelas():
    TABELAS = {
        # Cadastro de usuários
        # Configuração de personalização para cada usuário
        'users': """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_usuario TEXT,
            senha_hash TEXT,
            email TEXT,
            telefone TEXT,
            estado TEXT,
            cidade TEXT,
            comunidade TEXT
            );""",
        
        # Cadaastro extras como lote, raca, fornecedor, cliente, insumo, estoque...
        # 'tipo' receberá o nome de uso da linha. Ex: lote, raca...
        'outros': """CREATE TABLE IF NOT EXISTS outros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            a TEXT,
            b TEXT,
            c TEXT
            );""",
        # Histórico de compra/venda de animais
        'animais': """CREATE TABLE IF NOT EXISTS animais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        # Histórico de compra/consumo de insumos
        'insumo': """ CREATE TABLE IF NOT EXISTS insumo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_movimentacao TEXT,
            descrisao TEXT,
            data TEXT,
            lote TEXT,
            quantidade TEXT,
            valor_unitario TEXT,
            observacao TEXT,
            em_estoque TEXT
        );""",
        # Histórico de comportamento/vacina/tratamento aos animais
        'saude': """ CREATE TABLE IF NOT EXISTS saude (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            animal TEXT,
            data TEXT,
            peso TEXT,
            comportamento TEXT,
            medicamento TEXT,
            valor_inspecao_veterinaria TEXT,
            observacao TEXT
        );"""
    }
    return TABELAS
