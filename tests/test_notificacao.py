from decimal import Decimal

from rastreador import notificacao
from rastreador.notificacao import enviar_email, montar_email

PRODUTO = {"nome": "Livro", "url": "https://exemplo.com/livro"}


def test_monta_email_com_precos_e_link():
    mensagem = montar_email(
        PRODUTO, Decimal("54.90"), Decimal("38.40"), "robo@gmail.com", "eu@gmail.com"
    )

    assert mensagem["Subject"] == "O preço caiu: Livro por R$ 38,40"
    assert mensagem["From"] == "robo@gmail.com"
    assert mensagem["To"] == "eu@gmail.com"
    corpo = mensagem.get_content()
    assert "Antes: R$ 54,90" in corpo
    assert "Agora: R$ 38,40" in corpo
    assert "Economia: R$ 16,50" in corpo
    assert "https://exemplo.com/livro" in corpo


class GmailFalso:
    """Imita o servidor do Gmail: anota o login e a mensagem, sem enviar nada de verdade."""

    ultimo = None

    def __init__(self, servidor, porta):
        self.servidor = servidor
        self.porta = porta
        self.login_usado = None
        self.mensagem_enviada = None
        GmailFalso.ultimo = self

    def __enter__(self):
        return self

    def __exit__(self, *erro):
        return False

    def login(self, usuario, senha):
        self.login_usado = (usuario, senha)

    def send_message(self, mensagem):
        self.mensagem_enviada = mensagem


def test_envia_pelo_gmail_com_login(monkeypatch):
    monkeypatch.setattr(notificacao.smtplib, "SMTP_SSL", GmailFalso)
    mensagem = montar_email(PRODUTO, Decimal("10"), Decimal("5"), "robo@gmail.com", "eu@gmail.com")

    enviar_email(mensagem, "robo@gmail.com", "senhadeapp")

    gmail = GmailFalso.ultimo
    assert (gmail.servidor, gmail.porta) == ("smtp.gmail.com", 465)
    assert gmail.login_usado == ("robo@gmail.com", "senhadeapp")
    assert gmail.mensagem_enviada is mensagem
