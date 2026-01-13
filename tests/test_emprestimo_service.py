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

def test_paginacao_emprestimos_atuais(db_session):
    usuarios = [
        UsuarioService.criar_usuario(
            db_session, f"User{i}", PerfilAcesso.USUARIO
        )
        for i in range(2)
    ]

    livros = [
        LivroService.criar_livro(
            db_session,
            f"Livro {i}",
            "Autor",
            CategoriaLivro.TECNICO,
            1
        )
        for i in range(6)
    ]

    # 3 empréstimos para cada usuário (respeita regra)
    EmprestimoService.realizar_emprestimo(db_session, usuarios[0].id_usuario, livros[0].id_livro)
    EmprestimoService.realizar_emprestimo(db_session, usuarios[0].id_usuario, livros[1].id_livro)
    EmprestimoService.realizar_emprestimo(db_session, usuarios[0].id_usuario, livros[2].id_livro)

    EmprestimoService.realizar_emprestimo(db_session, usuarios[1].id_usuario, livros[3].id_livro)
    EmprestimoService.realizar_emprestimo(db_session, usuarios[1].id_usuario, livros[4].id_livro)
    EmprestimoService.realizar_emprestimo(db_session, usuarios[1].id_usuario, livros[5].id_livro)

    emprestimos_page_1 = EmprestimoService.listar_emprestimos_atuais(
        db_session, page=1, size=3
    )

    emprestimos_page_2 = EmprestimoService.listar_emprestimos_atuais(
        db_session, page=2, size=3
    )

    assert len(emprestimos_page_1) == 3
    assert len(emprestimos_page_2) == 3

def test_emprestimo_usuario_inexistente(db_session):
    livro = LivroService.criar_livro(
        db_session, "Livro", "Autor", CategoriaLivro.TECNICO, 1
    )

    with pytest.raises(ValueError):
        EmprestimoService.realizar_emprestimo(
            db_session, 999, livro.id_livro
        )

def test_emprestimo_livro_inexistente(db_session):
    usuario = UsuarioService.criar_usuario(
        db_session, "Ana", PerfilAcesso.USUARIO
    )

    with pytest.raises(ValueError):
        EmprestimoService.realizar_emprestimo(
            db_session, usuario.id_usuario, 999
        )

def test_emprestimo_sem_copias_disponiveis(db_session):
    usuario = UsuarioService.criar_usuario(
        db_session, "Ana", PerfilAcesso.USUARIO
    )

    livro = LivroService.criar_livro(
        db_session, "Livro", "Autor", CategoriaLivro.TECNICO, 1
    )

    EmprestimoService.realizar_emprestimo(
        db_session, usuario.id_usuario, livro.id_livro
    )

    with pytest.raises(ValueError):
        EmprestimoService.realizar_emprestimo(
            db_session, usuario.id_usuario, livro.id_livro
        )

def test_devolver_emprestimo_inexistente(db_session):
    with pytest.raises(ValueError):
        EmprestimoService.devolver_livro(db_session, 999)

def test_devolver_emprestimo_ja_devolvido(db_session):
    usuario = UsuarioService.criar_usuario(
        db_session, "Ana", PerfilAcesso.USUARIO
    )

    livro = LivroService.criar_livro(
        db_session, "Livro", "Autor", CategoriaLivro.TECNICO, 1
    )

    emprestimo = EmprestimoService.realizar_emprestimo(
        db_session, usuario.id_usuario, livro.id_livro
    )

    EmprestimoService.devolver_livro(db_session, emprestimo.id_emprestimo)

    with pytest.raises(ValueError):
        EmprestimoService.devolver_livro(db_session, emprestimo.id_emprestimo)

def test_devolver_emprestimo_ja_devolvido(db_session):
    usuario = UsuarioService.criar_usuario(
        db_session, "Ana", PerfilAcesso.USUARIO
    )

    livro = LivroService.criar_livro(
        db_session, "Livro", "Autor", CategoriaLivro.TECNICO, 1
    )

    emprestimo = EmprestimoService.realizar_emprestimo(
        db_session, usuario.id_usuario, livro.id_livro
    )

    EmprestimoService.devolver_livro(db_session, emprestimo.id_emprestimo)

    with pytest.raises(ValueError):
        EmprestimoService.devolver_livro(db_session, emprestimo.id_emprestimo)

from datetime import date, timedelta

def test_multa_por_atraso(db_session):
    usuario = UsuarioService.criar_usuario(
        db_session, "Ana", PerfilAcesso.USUARIO
    )

    livro = LivroService.criar_livro(
        db_session, "Livro", "Autor", CategoriaLivro.TECNICO, 1
    )

    data_passada = date.today() - timedelta(days=20)

    emprestimo = EmprestimoService.realizar_emprestimo(
        db_session,
        usuario.id_usuario,
        livro.id_livro,
        data_emprestimo=data_passada
    )

    emprestimo = EmprestimoService.devolver_livro(
        db_session, emprestimo.id_emprestimo
    )

    assert emprestimo.multa > 0
    assert emprestimo.status == "ATRASADO"
