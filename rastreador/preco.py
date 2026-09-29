"""Leitura do preço de um produto a partir da página da loja."""

from decimal import Decimal, InvalidOperation

import requests
from bs4 import BeautifulSoup

# Algumas lojas bloqueiam acessos que não parecem vir de um navegador.
# Este cabeçalho faz o robô se apresentar como um navegador comum.
CABECALHOS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9",
}

# Etiquetas <meta> onde as lojas costumam informar o preço (padrões schema.org e Open Graph).
# O robô tenta uma por uma, na ordem.
ETIQUETAS_DE_PRECO = [
    {"itemprop": "price"},
    {"property": "product:price:amount"},
    {"property": "og:price:amount"},
]


def baixar_pagina(url):
    """Baixa o HTML (o código) da página do produto."""
    resposta = requests.get(url, headers=CABECALHOS, timeout=30)
    resposta.raise_for_status()  # dá erro se a loja responder com falha (ex.: 404, 500)
    return resposta.text


def converter_preco(texto):
    """Transforma um texto como 'R$ 1.234,56' ou '38.40' em número (Decimal)."""
    limpo = texto.replace("R$", "").replace("\xa0", "").strip()
    if "," in limpo:
        # formato brasileiro: ponto separa milhar e vírgula separa centavos
        limpo = limpo.replace(".", "").replace(",", ".")
    try:
        return Decimal(limpo)
    except InvalidOperation:
        raise ValueError(f"Não consegui entender o preço '{texto}'.")


def extrair_preco(html):
    """Procura o preço dentro do HTML da página."""
    pagina = BeautifulSoup(html, "html.parser")
    for atributos in ETIQUETAS_DE_PRECO:
        etiqueta = pagina.find("meta", attrs=atributos)
        if etiqueta and etiqueta.get("content"):
            return converter_preco(etiqueta["content"])
    raise ValueError("Não encontrei o preço na página.")


def ler_preco(url):
    """Baixa a página e devolve o preço do produto."""
    return extrair_preco(baixar_pagina(url))


def formatar_reais(valor):
    """Mostra um número no formato brasileiro: Decimal('1234.5') -> 'R$ 1.234,50'."""
    texto = f"{valor:,.2f}"  # '1,234.50'
    return "R$ " + texto.replace(",", "_").replace(".", ",").replace("_", ".")
