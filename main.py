"""Ponto de partida do robô. Rode com: python main.py"""

from rastreador.banco import buscar_ultimo_preco, conectar, salvar_preco
from rastreador.comparacao import CAIU, PRIMEIRA_LEITURA, SUBIU, comparar
from rastreador.config import carregar_produtos
from rastreador.notificacao import avisar_queda
from rastreador.preco import formatar_reais, ler_preco


def descrever(resultado, anterior, atual):
    """Monta a frase que aparece na tela para cada produto."""
    if resultado == PRIMEIRA_LEITURA:
        return f"{formatar_reais(atual)} (primeira leitura, nada para comparar)"
    if resultado == CAIU:
        return f"{formatar_reais(atual)} — CAIU! (antes: {formatar_reais(anterior)})"
    if resultado == SUBIU:
        return f"{formatar_reais(atual)} — subiu (antes: {formatar_reais(anterior)})"
    return f"{formatar_reais(atual)} — sem mudança"


def main():
    produtos = carregar_produtos()
    banco = conectar()
    houve_erro = False
    print(f"Verificando {len(produtos)} produto(s)...")
    for produto in produtos:
        # Se um produto der erro, mostramos o problema e seguimos para o próximo.
        try:
            atual = ler_preco(produto["url"])
            anterior = buscar_ultimo_preco(banco, produto["url"])  # busca ANTES de gravar o de hoje
            salvar_preco(banco, produto, atual)
            resultado = comparar(anterior, atual)
            print(f"- {produto['nome']}: {descrever(resultado, anterior, atual)}")
            if resultado == CAIU:
                avisar_queda(produto, anterior, atual)
                print("  E-mail de alerta enviado.")
        except Exception as erro:
            print(f"- {produto['nome']}: ERRO ({erro})")
            houve_erro = True

    # Termina com código 1 ("falhou") se algum produto deu erro.
    # Assim o GitHub Actions marca a execução com ❌ e avisa você por e-mail.
    return 1 if houve_erro else 0


if __name__ == "__main__":
    raise SystemExit(main())
