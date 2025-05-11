import pandas as pd
import json
import os

class ManagerCSV:
    def __init__(self, arquivo, colunas):
        """
        Inicializa o gerenciador de CSV.

        Args:
            arquivo (str): Nome do arquivo CSV.
            colunas (list[str]): Lista de colunas (sem incluir 'id', que é automático).
        """

        self.arquivo = arquivo
        self.colunas = ['id'] + colunas
        if not os.path.exists(self.arquivo):
            df = pd.DataFrame(columns=self.colunas)
            df.to_csv(self.arquivo, index=False)

    def _carregar(self):
        return pd.read_csv(self.arquivo)

    def _salvar(self, df):
        df.to_csv(self.arquivo, index=False)

    def adicionar(self, dados):
        """Adiciona um novo registro com ID automático.

        Args:
            dados (dict): Dicionário com os dados (sem 'id').
        """
        
        df = self._carregar()
        novo_id = 1 if df.empty else df['id'].max() + 1
        dados_com_id = {'id': novo_id, **dados}

        novo_df = pd.DataFrame([dados_com_id])
        df = pd.concat([df, novo_df], ignore_index=True)

        self._salvar(df)

    def ler(self):
        """Retorna todos os registros."""
        return self._carregar()

    def buscar(self, campo, valor):
        """Busca registros com base no campo e valor.

        Args:
            campo (str): Onde procurar.
            valor (str): O que procurar.
        """
        df = self._carregar()
        return df[df[campo] == valor]

    def editar(self, id_alvo, novos_dados):
        """
            Edita um registro existente no arquivo CSV com base no ID fornecido. A função carrega o DataFrame
            correspondente, localiza o registro com o ID especificado e atualiza os campos informados no 
            dicionário novos_dados. Caso o ID não seja encontrado, uma exceção é lançada.

            Parâmetros:
                id_alvo (int): O ID do registro que se deseja editar.
                novos_dados (dict): Dicionário contendo os campos e os novos valores a serem atualizados.

            Exceções:
                ValueError: Lançada quando o ID especificado não é encontrado no arquivo.

            Efeitos colaterais:
                O arquivo CSV será sobrescrito com os dados atualizados, caso o ID exista.
        """
        df = self._carregar()

        if id_alvo in df['id'].values:
            for campo, valor in novos_dados.items():
                df.loc[df['id'] == id_alvo, campo] = valor
            self._salvar(df)
        else:
            raise ValueError(f"ID {id_alvo} não encontrado.")

    def excluir(self, id_alvo):
        """Exclui um registro com base no ID.

        Args:
            id_alvo (int): Id para excluir.
        """
        df = self._carregar()
        df = df[df['id'] != id_alvo]
        self._salvar(df)

# import json
# import os

class ManagerJSON:
    """
    Classe para gerenciar um único arquivo JSON com múltiplas categorias de dados,
    como 'lote', 'cliente', 'fornecedor', etc.
    """

    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = os.path.join('data', 'json', caminho_arquivo)
        self._garantir_arquivo()
        self.dados = self._carregar_dados()

    def _garantir_arquivo(self):
        """
        Garante que o diretório e o arquivo JSON de dados existam.

        Se o diretório especificado no caminho do arquivo não existir, ele será criado. 
        Em seguida, se o arquivo de dados também não existir, será criado um arquivo JSON vazio 
        contendo um dicionário inicial ({}).

        Efeitos colaterais:
            - Criação do diretório onde o arquivo será armazenado, se não existir.
            - Criação de um arquivo JSON vazio no caminho especificado, caso ainda não exista.
        """

        diretorio = os.path.dirname(self.caminho_arquivo)
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
        if not os.path.exists(self.caminho_arquivo):
            with open(self.caminho_arquivo, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=4)

    def _carregar_dados(self):
        with open(self.caminho_arquivo, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    def salvar(self):
        with open(self.caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(self.dados, f, ensure_ascii=False, indent=4)

    def atualizar_dado(self, categoria, valor):
        """
        Adiciona um novo valor a uma categoria específica, atribuindo um ID numérico automático.

        Se a categoria ainda não existir no dicionário de dados, ela será criada. 
        O novo valor será armazenado com um ID sequencial baseado nos IDs já existentes dentro da categoria.

        Parâmetros:
            categoria (str): Nome da categoria onde o valor será armazenado (ex: 'lote', 'cliente').
            valor (any): Dado a ser salvo na categoria, podendo ser string, dicionário ou outro tipo serializável.

        Retorna:
            str: O ID gerado automaticamente para o novo valor.

        Efeitos colaterais:
            - Atualiza o dicionário interno de dados.
            - Persiste os dados atualizados chamando o método salvar().
        """
        if categoria not in self.dados:
            self.dados[categoria] = {}

        if self.dados[categoria]:
            novo_id = str(int(max(self.dados[categoria].keys(), key=int)) + 1)
        else:
            novo_id = "1"

        self.dados[categoria][novo_id] = valor
        self.salvar()
        return novo_id

    def obter_dado(self, categoria, chave, padrao=None):
        """
        Retorna um dado específico armazenado dentro de uma categoria, utilizando o ID como chave.

        Caso a categoria ou a chave não existam, será retornado o valor especificado em padrao 
        (ou None, se não for informado).

        Parâmetros:
            categoria (str): Nome da categoria onde o dado está armazenado.
            chave (str): ID do item a ser recuperado.
            padrao (any, opcional): Valor a ser retornado caso o dado não seja encontrado. Padrão é None.

        Retorna:
            any: O valor armazenado correspondente à chave dentro da categoria, ou o valor padrão se não existir.
        """
        return self.dados.get(categoria, {}).get(chave, padrao)

    def deletar_dado(self, categoria, chave):
        """
        Remove um item de uma categoria específica com base na chave (ID).

        Se a categoria e a chave existirem no dicionário de dados, o item será removido 
        e os dados atualizados serão salvos. Caso contrário, uma mensagem de erro será retornada.

        Parâmetros:
            categoria (str): Nome da categoria de onde o item será removido.
            chave (str ou int): ID do item a ser removido. Aceita inteiro, mas será convertido para string.

        Retorna:
            str: Mensagem indicando se a exclusão foi realizada com sucesso ou se o item não foi encontrado.
        """
        if type(chave) is int: chave = str(chave)
        if categoria in self.dados.keys() and chave in self.dados[categoria].keys():
            del self.dados[categoria][chave]
            self.salvar()
            return f'Registro {chave} de {categoria} deletado com sucesso!'
        return f'Registro {chave} de {categoria} não encontrado!'

    def limpar_categoria(self, categoria):
        """
        Remove todos os dados armazenados em uma categoria específica.

        Se a categoria existir no dicionário de dados, todos os registros associados a ela 
        serão apagados e as alterações serão salvas no arquivo correspondente.

        Parâmetros:
            categoria (str): Nome da categoria que deve ser limpa.

        Efeitos colaterais:
            - A categoria é esvaziada no dicionário interno.
            - As alterações são persistidas chamando o método salvar().
        """
        if categoria in self.dados:
            self.dados[categoria] = {}
            self.salvar()

    def formatar_dados(self, categoria):
        """
        Retorna os dados de uma categoria em formato de texto legível.

        Se a categoria estiver vazia ou não existir, informa que não há dados.
        Caso contrário, exibe os dados com identação e organização por ID.

        Parâmetros:
            categoria (str): Nome da categoria cujos dados devem ser formatados (ex: 'lote', 'cliente').

        Retorna:
            str: Representação formatada em texto dos dados da categoria.
        """
        if categoria not in self.dados or not self.dados[categoria]:
            return f"{categoria}\n  Nenhum dado encontrado."

        linhas = [categoria]
        for chave, valor in self.dados[categoria].items():
            linhas.append(f"  ID: {chave}")
            if isinstance(valor, dict):
                for k, v in valor.items():
                    linhas.append(f"    {k}: {v}")
            else:
                linhas.append(f"    valor: {valor}")
        return "\n".join(linhas)
