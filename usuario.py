import sqlite3
import hashlib
import os

class UserManager:
    def __init__(self, db_path='data/users.db'):
        """
        Inicializa o gerenciador de usuários.
        Cria o diretório 'data/' se não existir e conecta ao banco de dados.
        Cria a tabela 'users' se ela não existir.
        """
        self.db_path = db_path
        self._ensure_data_directory()
        self._create_table()

    def _ensure_data_directory(self):
        """Garanto que o diretório 'data/' exista."""
        data_dir = os.path.dirname(self.db_path)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
            # print(f"Diretório '{data_dir}' criado.")

    def _get_db_connection(self):
        """Obtenho uma conexão com o banco de dados."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row # Para acessar colunas por nome
        return conn

    def _create_table(self):
        """Crio a tabela 'users' se ela não existir."""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        # print("Tabela 'users' verificada/criada com sucesso.")

    def _hash_password(self, password):
        """Gero o hash da senha usando SHA256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
        """
        Cadastra um novo usuário no banco de dados.
        Retorno True em caso de sucesso, False se o usuário já existir.
        """
        conn = self._get_db_connection()
        cursor = conn.cursor()
        try:
            password_hash = self._hash_password(password)
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                           (username, password_hash))
            conn.commit()
            return True, f"Usuário '{username}' cadastrado com sucesso."
        except sqlite3.IntegrityError:
            return False, f"Erro: Usuário '{username}' já existe."
        finally:
            conn.close()

    def login_user(self, username, password):
        """
        Verifica as credenciais do usuário.
        Se corretas, retorna True e o ID real do usuário (do banco de dados).
        Caso contrário, retorna False e uma mensagem de erro.
        """
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            # user_data['id'] é o ID real do usuário do banco de dados
            user_id = user_data['id'] 
            stored_password_hash = user_data['password_hash']
            input_password_hash = self._hash_password(password) # Certifique-se de que _hash_password use o mesmo algoritmo de hash para verificação

            # Em um cenário de produção REAL, você usaria uma biblioteca como bcrypt:
            # if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
            if stored_password_hash == input_password_hash: # Para o exemplo, mantendo sua comparação de hash
                # Login bem-sucedido! Retorna True e o ID real do usuário
                # print(f"Login bem-sucedido para '{username}'. ID do Usuário: {user_id}")
                return True, user_id
            else:
                return False, f"Erro de login para '{username}': Senha incorreta."
        else:
            return False, f"Erro de login: Usuário '{username}' não encontrado."

# --- Exemplo de Uso ---
if __name__ == "__main__":
    # Limpa o banco de dados existente para testar do zero
    if os.path.exists('data/users.db'):
        os.remove('data/users.db')
        print("Banco de dados existente removido para novo teste.")

    user_manager = UserManager()

    print("\n--- Teste de Cadastro ---")
    user_manager.register_user("admin", "senha123")
    user_manager.register_user("usuario1", "minhasenha")
    user_manager.register_user("admin", "outrasenha") # Tentativa de cadastrar usuário existente

    print("\n--- Teste de Login ---")
    session_id_admin = user_manager.login_user("admin", "senha123")
    if session_id_admin:
        print(f"Admin logado com sucesso! ID de sessão: {session_id_admin}")

    session_id_fail_pass = user_manager.login_user("admin", "senhaerrada")
    if not session_id_fail_pass:
        print("Login falhou para 'admin' com senha incorreta (esperado).")

    session_id_fail_user = user_manager.login_user("usuario_nao_existe", "qualquersenha")
    if not session_id_fail_user:
        print("Login falhou para usuário inexistente (esperado).")

    session_id_user1 = user_manager.login_user("usuario1", "minhasenha")
    if session_id_user1:
        print(f"Usuário1 logado com sucesso! ID de sessão: {session_id_user1}")