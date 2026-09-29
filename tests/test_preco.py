from decimal import Decimal

import pytest

from rastreador.preco import converter_preco, extrair_preco, formatar_reais

# Trecho copiado da página real da Livrarias Curitiba (simplificado).
HTML_LIVRARIAS_CURITIBA = """
<html><body>
  <div itemprop="offers" itemscope itemtype="http://schema.org/Offer">
    <meta content="BRL" itemprop="priceCurrency" />
    <meta itemprop="price" content="38.40" />
  </div>
  <strong class="skuBestPrice">R$ 38,40</strong>
</body></html>
"""


def test_extrai_preco_da_pagina_da_livraria():
    assert extrair_preco(HTML_LIVRARIAS_CURITIBA) == Decimal("38.40")


def test_extrai_preco_no_padrao_open_graph():
    html = '<html><head><meta property="product:price:amount" content="99,90"></head></html>'
    assert extrair_preco(html) == Decimal("99.90")


def test_da_erro_claro_quando_nao_ha_preco():
    with pytest.raises(ValueError, match="Não encontrei o preço"):
        extrair_preco("<html><body>Produto esgotado</body></html>")


@pytest.mark.parametrize(
    "texto, esperado",
    [
        ("38.40", Decimal("38.40")),
        ("38,40", Decimal("38.40")),
        ("R$ 38,40", Decimal("38.40")),
        ("R$ 1.234,56", Decimal("1234.56")),
    ],
)
def test_converte_varios_formatos_de_preco(texto, esperado):
    assert converter_preco(texto) == esperado


def test_recusa_texto_que_nao_e_preco():
    with pytest.raises(ValueError):
        converter_preco("grátis")


def test_formata_em_reais():
    assert formatar_reais(Decimal("38.4")) == "R$ 38,40"
    assert formatar_reais(Decimal("1234.56")) == "R$ 1.234,56"
