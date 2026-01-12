from app.services.service_livro import LivroService


def test_criar_livro(db_session):
    livro = LivroService.criar_livro(
        db=db_session,
        titulo="As aventuras do Manto Celeste",
        autor="Roberto Magalhães",
        categoria="Romance",
        qtd_copias=5,
        localizacao="A1"
    )

    assert livro.id_livro is not None
    assert livro.qtd_copias == 5
    assert livro.copias_disponiveis == 5
