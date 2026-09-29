from decimal import Decimal

from rastreador.banco import buscar_ultimo_preco, salvar_preco


class Resposta:
    def __init__(self, data):
        self.data = data


class ClienteFalso:
    """Imita o cliente do Supabase para testar sem acessar a internet.

    Em vez de conversar com o banco de verdade, ele anota o que recebeu
    e devolve as linhas que definimos no teste.
    """

    def __init__(self, linhas=None):
        self.linhas = linhas or []
        self.tabela_usada = None
        self.dados_inseridos = None
        self.filtros = {}

    def table(self, nome):
        self.tabela_usada = nome
        return self

    def insert(self, dados):
        self.dados_inseridos = dados
        return self

    def select(self, colunas):
        return self

    def eq(self, coluna, valor):
        self.filtros[coluna] = valor
        return self

    def order(self, coluna, desc=False):
        self.filtros["ordem"] = (coluna, desc)
        return self

    def limit(self, quantidade):
        self.filtros["limite"] = quantidade
        return self

    def execute(self):
        return Resposta(self.linhas)


def test_salva_preco_na_tabela_precos():
    cliente = ClienteFalso()
    produto = {"nome": "Livro", "url": "https://exemplo.com/livro"}

    salvar_preco(cliente, produto, Decimal("38.40"))

    assert cliente.tabela_usada == "precos"
    assert cliente.dados_inseridos == {
        "produto_nome": "Livro",
        "produto_url": "https://exemplo.com/livro",
        "preco": "38.40",
    }


def test_busca_o_preco_mais_recente_do_produto():
    cliente = ClienteFalso(linhas=[{"preco": 38.4}])

    preco = buscar_ultimo_preco(cliente, "https://exemplo.com/livro")

    assert preco == Decimal("38.4")
    assert cliente.filtros == {
        "produto_url": "https://exemplo.com/livro",
        "ordem": ("coletado_em", True),  # do mais novo para o mais antigo
        "limite": 1,
    }


def test_devolve_none_quando_nao_ha_preco_guardado():
    cliente = ClienteFalso(linhas=[])
    assert buscar_ultimo_preco(cliente, "https://exemplo.com/livro") is None
