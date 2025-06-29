-- 1. Comando: CREATE TABLE
-- Cria uma tabela 'clientes' se ela ainda não existir.
-- Usamos IF NOT EXISTS para evitar erros se a tabela já existir.
-- CREATE TABLE IF NOT EXISTS clientes (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     nome TEXT NOT NULL,
--     email TEXT UNIQUE,
--     data_cadastro TEXT DEFAULT CURRENT_TIMESTAMP
-- );

-- Cria uma tabela 'pedidos' se ela ainda não existir, com uma chave estrangeira para 'clientes'.
-- CREATE TABLE IF NOT EXISTS pedidos (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     cliente_id INTEGER NOT NULL,
--     produto TEXT NOT NULL,
--     valor REAL NOT NULL,
--     data_pedido TEXT DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (cliente_id) REFERENCES clientes(id)
-- );

-- 2. Comando: INSERT INTO
-- Insere novos registros na tabela 'clientes'.
-- INSERT INTO clientes (nome, email) VALUES ('Alice Silva', 'alice@example.com');
-- INSERT INTO clientes (nome, email) VALUES ('Bruno Costa', 'bruno@example.com');
-- INSERT INTO clientes (nome, email) VALUES ('Carla Dias', 'carla@example.com');

-- Insere novos registros na tabela 'pedidos'.
-- Certifique-se de que os 'cliente_id' existam na tabela 'clientes'.
-- INSERT INTO pedidos (cliente_id, produto, valor) VALUES (1, 'Smartphone X', 1500.00);
-- INSERT INTO pedidos (cliente_id, produto, valor) VALUES (1, 'Capa de Smartphone', 50.00);
-- INSERT INTO pedidos (cliente_id, produto, valor) VALUES (2, 'Fone de Ouvido', 200.00);
-- INSERT INTO pedidos (cliente_id, produto, valor) VALUES (3, 'Smart TV 50"', 3000.00);

-- 3. Comando: SELECT
-- Seleciona todos os clientes da tabela 'clientes'.
-- SELECT * FROM clientes;

-- Seleciona clientes com um nome específico.
-- SELECT id, nome, email FROM clientes WHERE nome = 'Alice Silva';

-- Seleciona pedidos com valor maior que 1000.
-- SELECT produto, valor FROM pedidos WHERE valor > 1000;

-- 4. Comando: UPDATE
-- Atualiza o email de um cliente.
-- UPDATE clientes SET email = 'alice.silva@newemail.com' WHERE nome = 'Alice Silva';

-- Atualiza o valor de um produto específico.
-- UPDATE pedidos SET valor = 250.00 WHERE produto = 'Fone de Ouvido';

-- 5. Comando: SELECT com JOIN
-- Seleciona informações combinadas das tabelas 'clientes' e 'pedidos'.
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
-- Isso cria uma nova tabela 'clientes_vip' com dados selecionados da tabela 'clientes'.
-- CREATE TABLE IF NOT EXISTS clientes_vip AS
-- SELECT id, nome, email
-- FROM clientes
-- WHERE nome LIKE 'Alice%';

-- Seleciona dados da nova tabela 'clientes_vip'.
-- SELECT * FROM clientes_vip;

-- 7. Comando: DELETE
-- Deleta um registro específico da tabela 'pedidos'.
-- Cuidado ao usar DELETE sem WHERE, pois ele remove todas as linhas da tabela!
-- DELETE FROM pedidos WHERE produto = 'Capa de Smartphone';

-- Deleta um cliente pelo nome (e quaisquer pedidos relacionados se configurado com CASCADE no FOREIGN KEY,
-- ou você precisaria deletar os pedidos primeiro).
-- DELETE FROM clientes WHERE nome = 'Bruno Costa';

-- 8. Comando: DROP TABLE (Cuidado! Isso remove a tabela e todos os seus dados)
-- Usado geralmente para limpar o ambiente de teste.
-- DROP TABLE IF EXISTS clientes;
-- DROP TABLE IF EXISTS pedidos;
-- DROP TABLE IF EXISTS clientes_vip;

-- 9. Comando: Listar todas as tabelas no banco de dados
-- Consulta a tabela mestra 'sqlite_master' que armazena informações sobre o schema.
SELECT name FROM sqlite_master WHERE type='table';

-- 10. Comando: Listar colunas de uma tabela específica (Ex: 'clientes')
-- O comando PRAGMA table_info(nome_da_tabela) retorna detalhes das colunas.
PRAGMA table_info(clientes);

-- 11. Comando: Listar colunas de outra tabela específica (Ex: 'pedidos')
PRAGMA table_info(pedidos);

-- 12. Comando: Listar colunas da tabela 'clientes_vip' (se ela foi criada)
PRAGMA table_info(clientes_vip);