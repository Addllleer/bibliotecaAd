from datetime import timedelta, date

from app.services.service_usuario import UsuarioService
from app.services.service_livro import LivroService
from app.services.service_emprestimo import EmprestimoService


def test_realizar_emprestimo_com_sucesso(db_session):
    usuario = UsuarioService.criar_usuario(db_session, "Renan", "COMUM")
    livro = LivroService.criar_livro(
        db_session, "Catequese ABC", "Renan da Silva", "Religião", 2
    )

    emprestimo = EmprestimoService.realizar_emprestimo(
        db_session,
        id_usuario=usuario.id_usuario,
        id_livro=livro.id_livro
    )

    assert emprestimo.status == "ATIVO"
    assert emprestimo.prazo_devolucao == date.today() + timedelta(days=14)


def test_limite_maximo_de_emprestimos(db_session):
    usuario = UsuarioService.criar_usuario(db_session, "Ana", "COMUM")
    livro = LivroService.criar_livro(
        db_session, "Fundamentos de Física", "Antônio Stark", "Técnico", 5
    )

    for _ in range(3):
        EmprestimoService.realizar_emprestimo(
            db_session,
            usuario.id_usuario,
            livro.id_livro
        )

    try:
        EmprestimoService.realizar_emprestimo(
            db_session,
            usuario.id_usuario,
            livro.id_livro
        )
        assert False
    except ValueError as e:
        assert "limite de empréstimos" in str(e)
