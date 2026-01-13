import pytest
from app.services.service_livro import LivroService
from app.domain.enums.categoria_livro import CategoriaLivro
from app.domain.enums.localizacao_livro import LocalizacaoLivro



def test_criar_livro(db_session):
    livro = LivroService.criar_livro(
        db=db_session,
        titulo="As aventuras do Manto Celeste",
        autor="Roberto Magalhães",
        categoria=CategoriaLivro.AVENTURA,
        qtd_copias=5,
        localizacao=LocalizacaoLivro.A1
    )

    assert livro.id_livro is not None
    assert livro.qtd_copias == 5
    assert livro.copias_disponiveis == 5

def test_listar_livros_retorna_lista(db_session):
    LivroService.criar_livro(
        db_session,
        "Livro A",
        "Autor A",
        CategoriaLivro.TECNICO,
        2
    )

    LivroService.criar_livro(
        db_session,
        "Livro B",
        "Autor B",
        CategoriaLivro.ROMANCE,
        1
    )

    livros = LivroService.listar_livros(db_session)

    assert isinstance(livros, list)
    assert len(livros) == 2
    assert livros[0].titulo == "Livro A"
    assert livros[1].titulo == "Livro B"

def test_listar_livros_paginacao(db_session):
    for i in range(12):
        LivroService.criar_livro(
            db_session,
            f"Livro {i}",
            "Autor",
            CategoriaLivro.TECNICO,
            1
        )

    livros_page_1 = LivroService.listar_livros(db_session, page=1, size=5)
    livros_page_2 = LivroService.listar_livros(db_session, page=2, size=5)

    assert len(livros_page_1) == 5
    assert len(livros_page_2) == 5

def test_buscar_livro_inexistente(db_session):
    with pytest.raises(LookupError):
        LivroService.buscar_livro(db_session, 999)

def test_criar_livro_quantidade_zero(db_session):
    with pytest.raises(ValueError):
        LivroService.criar_livro(
            db_session,
            "Livro Inválido",
            "Autor",
            CategoriaLivro.TECNICO,
            0
        )

def test_criar_livro_quantidade_negativa(db_session):
    with pytest.raises(ValueError):
        LivroService.criar_livro(
            db_session,
            "Livro Inválido",
            "Autor",
            CategoriaLivro.TECNICO,
            -1
        )

def test_criar_livro_titulo_vazio(db_session):
    with pytest.raises(ValueError):
        LivroService.criar_livro(
            db_session,
            "",
            "Autor",
            CategoriaLivro.TECNICO,
            1
        )

def test_criar_livro_titulo_vazio(db_session):
    with pytest.raises(ValueError):
        LivroService.criar_livro(
            db_session,
            "",
            "Autor",
            CategoriaLivro.TECNICO,
            1
        )

def test_listar_livros_pagina_vazia(db_session):
    livros = LivroService.listar_livros(
        db_session, page=10, size=10
    )

    assert livros == []

def test_listar_livros_paginacao_limite(db_session):
    for i in range(15):
        LivroService.criar_livro(
            db_session,
            f"Livro {i}",
            "Autor",
            CategoriaLivro.TECNICO,
            1
        )

    livros = LivroService.listar_livros(
        db_session, page=1, size=10
    )

    assert len(livros) == 10


