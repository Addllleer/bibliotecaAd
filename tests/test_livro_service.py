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

