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

