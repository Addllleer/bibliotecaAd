from sqlalchemy.orm import Session
from app.models.model_usuario import Usuario
from app.repositories.repository_usuario import UsuarioRepository


class UsuarioService:

    @staticmethod
    def criar_usuario(db: Session, nome: str, perfil_acesso: str) -> Usuario:
        usuario_existente = UsuarioRepository.get_by_nome(db, nome)

        if usuario_existente:
            raise ValueError("Usuário já existe")
        
        usuario = Usuario(
            nome=nome,
            perfil_acesso=perfil_acesso.value
        )
        return UsuarioRepository.create(db, usuario)

    @staticmethod
    def buscar_usuario(db: Session, id_usuario: int) -> Usuario | None:
        return UsuarioRepository.get_by_id(db, id_usuario)

    @staticmethod
    def listar_usuarios(db: Session, page: int = 1, size: int = 10):
        return UsuarioRepository.list_all(db, page, size)
