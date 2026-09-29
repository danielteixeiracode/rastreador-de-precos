import json

import pytest

from rastreador.config import carregar_produtos


def criar_arquivo(tmp_path, conteudo):
    caminho = tmp_path / "produtos.json"
    caminho.write_text(json.dumps(conteudo), encoding="utf-8")
    return caminho


def test_carrega_o_produtos_json_do_projeto():
    produtos = carregar_produtos()
    assert len(produtos) >= 1
    assert produtos[0]["url"].startswith("https://")


def test_aceita_lista_valida(tmp_path):
    caminho = criar_arquivo(tmp_path, [{"nome": "Livro", "url": "https://exemplo.com"}])
    assert carregar_produtos(caminho) == [{"nome": "Livro", "url": "https://exemplo.com"}]


def test_recusa_produto_sem_url(tmp_path):
    caminho = criar_arquivo(tmp_path, [{"nome": "Livro"}])
    with pytest.raises(ValueError, match="url"):
        carregar_produtos(caminho)


def test_recusa_arquivo_que_nao_e_lista(tmp_path):
    caminho = criar_arquivo(tmp_path, {"nome": "Livro", "url": "https://exemplo.com"})
    with pytest.raises(ValueError, match="lista"):
        carregar_produtos(caminho)
