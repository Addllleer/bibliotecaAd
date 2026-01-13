from sqlalchemy.orm import Session

from app.models.model_livro import Livro
from app.repositories.repository_livro import LivroRepository


class LivroService:

    @staticmethod
    def criar_livro(
        db: Session,
        titulo: str,
        autor: str,
        categoria: str,
        qtd_copias: int,
        localizacao: str | None = None
    ) -> Livro:

        livro = Livro(
            titulo=titulo,
            autor=autor,
            categoria=categoria.value,
            qtd_copias=qtd_copias,
            copias_disponiveis=qtd_copias,
            localizacao=localizacao.value if localizacao else None
        )

        return LivroRepository.create(db, livro)

    @staticmethod
    def buscar_livro(db: Session, id_livro: int) -> Livro | None:
        return LivroRepository.get_by_id(db, id_livro)

    @staticmethod
    def listar_livros(db: Session) -> list[Livro]:
        return LivroRepository.list_all(db)
