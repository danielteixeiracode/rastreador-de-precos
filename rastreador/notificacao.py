"""Envio do e-mail de alerta pelo Gmail."""

import smtplib
from email.message import EmailMessage

from rastreador.config import carregar_variavel
from rastreador.preco import formatar_reais

SERVIDOR_GMAIL = "smtp.gmail.com"
PORTA_GMAIL = 465  # porta com conexão criptografada (SSL)


def montar_email(produto, preco_anterior, preco_atual, remetente, destino):
    """Cria a mensagem de e-mail avisando que o preço caiu."""
    economia = preco_anterior - preco_atual

    mensagem = EmailMessage()
    mensagem["Subject"] = f"O preço caiu: {produto['nome']} por {formatar_reais(preco_atual)}"
    mensagem["From"] = remetente
    mensagem["To"] = destino
    mensagem.set_content(
        f"Boa notícia! O preço de \"{produto['nome']}\" caiu.\n"
        f"\n"
        f"Antes: {formatar_reais(preco_anterior)}\n"
        f"Agora: {formatar_reais(preco_atual)}\n"
        f"Economia: {formatar_reais(economia)}\n"
        f"\n"
        f"Ver o produto: {produto['url']}\n"
        f"\n"
        f"-- Enviado pelo seu Rastreador de Preços"
    )
    return mensagem


def enviar_email(mensagem, usuario, senha_app):
    """Entra no Gmail com a senha de app e envia a mensagem."""
    with smtplib.SMTP_SSL(SERVIDOR_GMAIL, PORTA_GMAIL) as servidor:
        servidor.login(usuario, senha_app)
        servidor.send_message(mensagem)


def avisar_queda(produto, preco_anterior, preco_atual):
    """Lê os dados do Gmail no .env, monta o e-mail e envia."""
    usuario = carregar_variavel("GMAIL_USUARIO")
    # O Google mostra a senha de app com espaços ("abcd efgh ijkl mnop"); removemos por garantia.
    senha_app = carregar_variavel("GMAIL_SENHA_APP").replace(" ", "")
    destino = carregar_variavel("EMAIL_DESTINO")

    mensagem = montar_email(produto, preco_anterior, preco_atual, usuario, destino)
    enviar_email(mensagem, usuario, senha_app)
