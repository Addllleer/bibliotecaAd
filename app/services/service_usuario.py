from sqlalchemy.orm import Session
from app.models.model_usuario import Usuario
from app.repositories.repository_usuario import UsuarioRepository
from app.domain.enums.perfil_acesso import PerfilAcesso
from app.logger import get_logger

logger = get_logger(__name__)


class UsuarioService:

    @staticmethod
    def criar_usuario(
        db: Session,
        nome: str,
        perfil_acesso: PerfilAcesso
    ) -> Usuario:

        logger.info(
            "Tentativa de criação de usuário | nome=%s | perfil=%s",
            nome,
            perfil_acesso.value
        )

        usuario_existente = UsuarioRepository.get_by_nome(db, nome)
        if usuario_existente:
            logger.warning(
                "Usuário já existe | nome=%s",
                nome
            )
            raise ValueError("Usuário já existe")

        usuario = Usuario(
            nome=nome,
            perfil_acesso=perfil_acesso.value
        )

        usuario_criado = UsuarioRepository.create(db, usuario)

        logger.info(
            "Usuário criado com sucesso | id=%s | nome=%s",
            usuario_criado.id_usuario,
            usuario_criado.nome
        )

        return usuario_criado
    
    @staticmethod
    def listar_usuarios(db: Session, page: int = 1, size: int = 10):
        offset = (page - 1) * size
        return (
            db.query(Usuario)
            .offset(offset)
            .limit(size)
            .all()
        )

    @staticmethod
    def buscar_usuario(db: Session, id_usuario: int):
        usuario = UsuarioRepository.get_by_id(db, id_usuario)

        if not usuario:
            raise ValueError("Usuário não encontrado")

        usuario.emprestimos = [
            e for e in usuario.emprestimos
            if e.status in ("ATIVO", "ATRASADO")
        ]

        return usuario



