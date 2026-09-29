"""Envia um e-mail de exemplo para conferir se o Gmail está configurado.

Rode com: python testar_email.py
Não mexe no banco de dados.
"""

from decimal import Decimal

from rastreador.notificacao import avisar_queda

produto_exemplo = {
    "nome": "TESTE - Produto de exemplo",
    "url": "https://www.livrariascuritiba.com.br/marco-aurelio---meditacoes-lv472246/p",
}

avisar_queda(produto_exemplo, Decimal("54.90"), Decimal("38.40"))
print("E-mail de teste enviado! Confira sua caixa de entrada (e a pasta de spam).")
