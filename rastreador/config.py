"""Leitura das configurações do projeto: lista de produtos e variáveis do .env."""

import json
import os
from pathlib import Path

from dotenv import load_dotenv

PASTA_PROJETO = Path(__file__).resolve().parent.parent
ARQUIVO_PRODUTOS = PASTA_PROJETO / "produtos.json"


def carregar_produtos(caminho=ARQUIVO_PRODUTOS):
    """Lê o produtos.json e devolve uma lista de produtos (cada um com 'nome' e 'url')."""
    with open(caminho, encoding="utf-8") as arquivo:
        produtos = json.load(arquivo)

    if not isinstance(produtos, list):
        raise ValueError("O produtos.json deve conter uma lista [ ... ] de produtos.")

    for posicao, produto in enumerate(produtos, start=1):
        for campo in ("nome", "url"):
            if not produto.get(campo):
                raise ValueError(f"O produto nº {posicao} está sem o campo '{campo}'.")

    return produtos


def carregar_variavel(nome):
    """Lê uma variável do arquivo .env (ou do ambiente). Dá erro claro se ela não existir."""
    load_dotenv(PASTA_PROJETO / ".env")
    valor = os.getenv(nome)
    if not valor:
        raise RuntimeError(f"A variável '{nome}' não foi definida no arquivo .env.")
    return valor
