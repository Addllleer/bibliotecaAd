from sqlalchemy.orm import Session

from app.models.model_usuario import Usuario
from app.repositories.repository_usuario import UsuarioRepository


class UsuarioService:

    @staticmethod
    def criar_usuario(db: Session, nome: str, perfil_acesso: str) -> Usuario:
        usuario = Usuario(
            nome=nome,
            perfil_acesso=perfil_acesso.value
        )
        return UsuarioRepository.create(db, usuario)

    @staticmethod
    def buscar_usuario(db: Session, id_usuario: int) -> Usuario | None:
        return UsuarioRepository.get_by_id(db, id_usuario)

    @staticmethod
    def listar_usuarios(db: Session) -> list[Usuario]:
        return UsuarioRepository.list_all(db)
