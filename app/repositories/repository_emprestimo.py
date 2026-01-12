from sqlalchemy.orm import Session
from app.models.model_emprestimo import Emprestimo


class EmprestimoRepository:

    @staticmethod
    def create(db: Session, emprestimo: Emprestimo) -> Emprestimo:
        db.add(emprestimo)
        db.commit()
        db.refresh(emprestimo)
        return emprestimo

    @staticmethod
    def get_by_id(db: Session, id_emprestimo: int) -> Emprestimo | None:
        return (
            db.query(Emprestimo)
            .filter(Emprestimo.id_emprestimo == id_emprestimo)
            .first()
        )

    @staticmethod
    def list_by_usuario(db: Session, id_usuario: int) -> list[Emprestimo]:
        return (
            db.query(Emprestimo)
            .filter(Emprestimo.id_usuario == id_usuario)
            .all()
        )
