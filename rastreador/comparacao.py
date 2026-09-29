"""Comparação entre o preço anterior e o preço de hoje."""

PRIMEIRA_LEITURA = "primeira leitura"
CAIU = "caiu"
SUBIU = "subiu"
IGUAL = "igual"


def comparar(preco_anterior, preco_atual):
    """Diz o que aconteceu com o preço: caiu, subiu, ficou igual ou é a primeira leitura."""
    if preco_anterior is None:
        return PRIMEIRA_LEITURA
    if preco_atual < preco_anterior:
        return CAIU
    if preco_atual > preco_anterior:
        return SUBIU
    return IGUAL
