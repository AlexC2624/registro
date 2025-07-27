import hashlib
from models import SQL

def _hash_password(password):
    """Gero o hash da senha usando SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(sql: SQL, username: str, password: str):
    """
    Cadastra um novo usuário no banco de dados.
    Retorno True em caso de sucesso, False se o usuário já existir.
    """
    try:
        password_hash = _hash_password(password)
        sql.inserir('users', ['username', 'password_hash'], [username, password_hash])
        return True, sql.cursor.lastrowid
    # except ValueError as e:
    #     return False, f"Erro: Usuário '{username}' já existe."
    finally:
        # sql.conn.close()
        pass

def login_user(sql: SQL, username: str, password: str):
    """
    Verifica as credenciais do usuário.
    Se corretas, retorna True e o ID real do usuário (do banco de dados).
    Caso contrário, retorna False e uma mensagem de erro.
    """
    user_data = sql.buscar_registro('users', 'username', username)
    # sql.conn.close()

    if user_data:
        # user_data['id'] é o ID real do usuário do banco de dados
        # print(f"Dados do usuário encontrado: {user_data}")
        user_data = user_data[0]
        user_id = user_data[0]
        stored_password_hash = user_data[2]
        input_password_hash = _hash_password(password) # Certifique-se de que _hash_password use o mesmo algoritmo de hash para verificação

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

def get_user_by_id(sql:SQL, user_id):
        """
        Retorna os dados do usuário pelo ID.
        Se encontrado, retorna um dicionário com os dados do usuário.
        Caso contrário, retorna None.
        """
        user_data = sql.buscar_registro('users', 'id', user_id)
        # sql.conn.close()
        if user_data:
            return {"id": user_data[0][0], "username": user_data[0][1]}
        else:
            return None

# --- Exemplo de Uso ---
if __name__ == "__main__": pass
