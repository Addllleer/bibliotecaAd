from sqlalchemy.orm import Session
from app.models.model_livro import Livro


class LivroRepository:

    @staticmethod
    def create(db: Session, livro: Livro) -> Livro:
        db.add(livro)
        db.commit()
        db.refresh(livro)
        return livro

    @staticmethod
    def get_by_id(db: Session, id_livro: int) -> Livro | None:
        return db.query(Livro).filter(Livro.id_livro == id_livro).first()

    @staticmethod
    def list_all(db: Session) -> list[Livro]:
        return db.query(Livro).all()

    @staticmethod
    def update(db: Session, livro: Livro) -> Livro:
        db.commit()
        db.refresh(livro)
        return livro
