from decimal import Decimal

from rastreador.comparacao import CAIU, IGUAL, PRIMEIRA_LEITURA, SUBIU, comparar


def test_primeira_leitura_quando_nao_ha_preco_anterior():
    assert comparar(None, Decimal("38.40")) == PRIMEIRA_LEITURA


def test_preco_caiu():
    assert comparar(Decimal("54.90"), Decimal("38.40")) == CAIU


def test_preco_subiu():
    assert comparar(Decimal("38.40"), Decimal("54.90")) == SUBIU


def test_preco_igual():
    assert comparar(Decimal("38.40"), Decimal("38.40")) == IGUAL


def test_um_centavo_a_menos_ja_conta_como_queda():
    assert comparar(Decimal("38.40"), Decimal("38.39")) == CAIU
