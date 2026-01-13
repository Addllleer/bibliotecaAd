import pytest
from app.services.service_usuario import UsuarioService
from app.domain.enums.perfil_acesso import PerfilAcesso



def test_criar_usuario(db_session):
    usuario = UsuarioService.criar_usuario(
        db=db_session,
        nome="Maria da Conceição",
        perfil_acesso=PerfilAcesso.USUARIO
    )

    assert usuario.id_usuario is not None
    assert usuario.nome == "Maria da Conceição"
    assert usuario.perfil_acesso == PerfilAcesso.USUARIO


def test_listar_usuarios(db_session):
    UsuarioService.criar_usuario(db_session, "A", PerfilAcesso.USUARIO)
    UsuarioService.criar_usuario(db_session, "B", PerfilAcesso.ADMIN)

    usuarios = UsuarioService.listar_usuarios(db_session)

    assert len(usuarios) == 2

def test_listar_usuarios_retorna_lista(db_session):
    UsuarioService.criar_usuario(
        db_session, "João", PerfilAcesso.USUARIO
    )
    UsuarioService.criar_usuario(
        db_session, "Maria", PerfilAcesso.ADMIN
    )

    usuarios = UsuarioService.listar_usuarios(db_session)

    assert isinstance(usuarios, list)
    assert len(usuarios) == 2
    assert usuarios[0].nome == "João"
    assert usuarios[1].nome == "Maria"

def test_listar_usuarios_paginacao(db_session):
    for i in range(15):
        UsuarioService.criar_usuario(
            db_session,
            f"Usuario{i}",
            PerfilAcesso.USUARIO
        )

    usuarios_page_1 = UsuarioService.listar_usuarios(db_session, page=1, size=10)
    usuarios_page_2 = UsuarioService.listar_usuarios(db_session, page=2, size=10)

    assert len(usuarios_page_1) == 10
    assert len(usuarios_page_2) == 5

def test_pagina_vazia_retorna_lista_vazia(db_session):
    usuarios = UsuarioService.listar_usuarios(db_session, page=99, size=10)
    assert usuarios == []

def test_criar_usuario_duplicado(db_session):
    UsuarioService.criar_usuario(
        db_session, "Duplicado", PerfilAcesso.USUARIO
    )

    with pytest.raises(ValueError) as exc:
        UsuarioService.criar_usuario(
            db_session, "Duplicado", PerfilAcesso.ADMIN
        )

    assert "Usuário já existe" in str(exc.value)

def test_buscar_usuario_inexistente(db_session):
    usuario = UsuarioService.buscar_usuario(db_session, 999)

    assert usuario is None

def test_listar_usuarios_pagina_vazia(db_session):
    usuarios = UsuarioService.listar_usuarios(
        db_session, page=10, size=10
    )

    assert usuarios == []

def test_listar_usuarios_page_maior_que_total(db_session):
    UsuarioService.criar_usuario(
        db_session, "A", PerfilAcesso.USUARIO
    )

    usuarios = UsuarioService.listar_usuarios(
        db_session, page=2, size=10
    )

    assert usuarios == []

