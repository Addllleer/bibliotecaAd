import pytest

from datetime import timedelta, date
from app.services.service_usuario import UsuarioService
from app.services.service_livro import LivroService
from app.services.service_emprestimo import EmprestimoService
from app.domain.enums.categoria_livro import CategoriaLivro
from app.domain.enums.localizacao_livro import LocalizacaoLivro
from app.domain.enums.perfil_acesso import PerfilAcesso
from app.repositories.repository_emprestimo import EmprestimoRepository



def test_limite_maximo_de_emprestimos(db_session):
    usuario = UsuarioService.criar_usuario(
        db_session, "Ana", PerfilAcesso.USUARIO
    )

    livros = [
        LivroService.criar_livro(
            db_session,
            f"Livro {i}",
            "Autor Teste",
            CategoriaLivro.TECNICO,
            1
        )
        for i in range(3)
    ]

    # Realiza 3 empréstimos válidos (livros diferentes)
    for livro in livros:
        EmprestimoService.realizar_emprestimo(
            db_session,
            usuario.id_usuario,
            livro.id_livro
        )

    # Cria um quarto livro
    livro_extra = LivroService.criar_livro(
        db_session,
        "Livro Extra",
        "Autor Teste",
        CategoriaLivro.TECNICO,
        1
    )

    # Tenta realizar o 4º empréstimo
    with pytest.raises(ValueError) as exc:
        EmprestimoService.realizar_emprestimo(
            db_session,
            usuario.id_usuario,
            livro_extra.id_livro
        )

    assert "limite de empréstimos" in str(exc.value)

def test_listar_emprestimos_por_usuario(db_session):
    usuario = UsuarioService.criar_usuario(
        db_session, "Carlos", PerfilAcesso.USUARIO
    )

    livro = LivroService.criar_livro(
        db_session,
        "Livro Teste",
        "Autor Teste",
        CategoriaLivro.TECNICO,
        1
    )

    emprestimo = EmprestimoService.realizar_emprestimo(
        db_session,
        usuario.id_usuario,
        livro.id_livro
    )

    emprestimos = EmprestimoRepository.list_by_usuario(
        db_session,
        usuario.id_usuario
    )

    assert isinstance(emprestimos, list)
    assert len(emprestimos) == 1
    assert emprestimos[0].id_emprestimo == emprestimo.id_emprestimo

