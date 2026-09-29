"""Comunicação com o banco de dados (Supabase)."""

from decimal import Decimal

from supabase import create_client

from rastreador.config import carregar_variavel

TABELA = "precos"


def conectar():
    """Abre a conexão com o Supabase usando a URL e a chave do arquivo .env."""
    return create_client(carregar_variavel("SUPABASE_URL"), carregar_variavel("SUPABASE_KEY"))


def buscar_ultimo_preco(cliente, url):
    """Devolve o preço mais recente guardado para este produto, ou None se ainda não houver nenhum."""
    resposta = (
        cliente.table(TABELA)
        .select("preco")
        .eq("produto_url", url)
        .order("coletado_em", desc=True)
        .limit(1)
        .execute()
    )
    if not resposta.data:
        return None
    # O banco devolve o preço como número comum (ex.: 38.4); convertemos para Decimal.
    return Decimal(str(resposta.data[0]["preco"]))


def salvar_preco(cliente, produto, preco):
    """Grava uma linha na tabela 'precos' com o preço lido hoje."""
    cliente.table(TABELA).insert(
        {
            "produto_nome": produto["nome"],
            "produto_url": produto["url"],
            # O Decimal vai como texto para não perder os centavos no caminho.
            "preco": str(preco),
        }
    ).execute()
