from sqlalchemy.orm import Session
from app.models.model_usuario import Usuario


class UsuarioRepository:

    @staticmethod
    def get_by_nome(db: Session, nome: str) -> Usuario | None:
        return db.query(Usuario).filter(Usuario.nome == nome).first()

    @staticmethod
    def create(db: Session, usuario: Usuario) -> Usuario:
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario

    @staticmethod
    def get_by_id(db: Session, id_usuario: int) -> Usuario | None:
        return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

    @staticmethod
    def list_all(db: Session) -> list[Usuario]:
        return db.query(Usuario).all()

    @staticmethod
    def count_emprestimos_ativos(db: Session, id_usuario: int) -> int:
        from app.models.model_emprestimo import Emprestimo
        return (
            db.query(Emprestimo)
            .filter(
                Emprestimo.id_usuario == id_usuario,
                Emprestimo.status.in_(["ATIVO", "ATRASADO"])
            )
            .count()
        )
