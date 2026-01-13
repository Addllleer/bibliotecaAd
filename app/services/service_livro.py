from sqlalchemy.orm import Session

from app.models.model_livro import Livro
from app.repositories.repository_livro import LivroRepository
from app.repositories.repository_usuario import UsuarioRepository


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

        if not titulo or not titulo.strip():
            raise ValueError("Título inválido")

        if not autor or not autor.strip():
            raise ValueError("Autor inválido")

        if qtd_copias <= 0:
            raise ValueError("Quantidade inválida")

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
    def listar_livros(db: Session, page: int = 1, size: int = 10):
        return LivroRepository.list_all(db, page, size)

    @staticmethod
    def listar_usuarios(db: Session, page: int = 1, size: int = 10):
        return UsuarioRepository.list_all(db, page, size)
    
    @staticmethod
    def buscar_livro(db: Session, id_livro: int):
        livro = LivroRepository.get_by_id(db, id_livro)
        if not livro:
            raise LookupError("Livro não encontrado")
        return livro


