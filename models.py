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
        Edita um registro com base no ID.

        Args:
            id_alvo (int): ID do registro a ser editado.
            novos_dados (dict): Dicionário com os campos a atualizar.
        
        Raise:
            ValueError: Se não encontrar o id.
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
        self.caminho_arquivo = caminho_arquivo
        self._garantir_arquivo()
        self.dados = self._carregar_dados()

    def _garantir_arquivo(self):
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
        Adiciona um valor a uma categoria específica com ID automático.

        :param categoria: Nome da categoria (ex: 'lote', 'cliente').
        :param valor: Dado a ser salvo.
        :return: ID gerado.
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
        Retorna um dado específico dentro de uma categoria.

        :param categoria: Nome da categoria.
        :param chave: ID do item.
        :param padrao: Valor padrão se não existir.
        """
        return self.dados.get(categoria, {}).get(chave, padrao)

    def deletar_dado(self, categoria, chave):
        """
        Remove um item de uma categoria.

        :param categoria: Nome da categoria.
        :param chave: ID do item.
        """
        if type(chave) is int: chave = str(chave)
        if categoria in self.dados.keys() and chave in self.dados[categoria].keys():
            del self.dados[categoria][chave]
            self.salvar()
            return f'Registro {chave} de {categoria} deletado com sucesso!'
        return f'Registro {chave} de {categoria} não encontrado!'

    def limpar_categoria(self, categoria):
        """
        Remove todos os dados de uma categoria específica.
        """
        if categoria in self.dados:
            self.dados[categoria] = {}
            self.salvar()

    def formatar_dados(self, categoria):
        """
        Retorna os dados formatados de uma categoria específica.

        :param categoria: Nome da categoria (ex: 'lote', 'cliente').
        :return: String formatada.
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
