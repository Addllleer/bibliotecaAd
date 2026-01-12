from app.services.service_usuario import UsuarioService


def test_criar_usuario(db_session):
    usuario = UsuarioService.criar_usuario(
        db=db_session,
        nome="Maria da Conceição",
        perfil_acesso="COMUM"
    )

    assert usuario.id_usuario is not None
    assert usuario.nome == "Maria da Conceição"
    assert usuario.perfil_acesso == "COMUM"


def test_listar_usuarios(db_session):
    UsuarioService.criar_usuario(db_session, "A", "COMUM")
    UsuarioService.criar_usuario(db_session, "B", "ADMIN")

    usuarios = UsuarioService.listar_usuarios(db_session)

    assert len(usuarios) == 2
