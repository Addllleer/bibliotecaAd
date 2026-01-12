from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.schema_livro import LivroCreate, LivroResponse
from app.services.service_livro import LivroService

router = APIRouter(prefix="/livros", tags=["Livros"])


@router.post("/", response_model=LivroResponse, status_code=status.HTTP_201_CREATED)
def criar_livro(livro: LivroCreate, db: Session = Depends(get_db)):
    return LivroService.criar_livro(
        db=db,
        titulo=livro.titulo,
        autor=livro.autor,
        categoria=livro.categoria,
        qtd_copias=livro.qtd_copias,
        localizacao=livro.localizacao
    )


@router.get("/{id_livro}", response_model=LivroResponse)
def buscar_livro(id_livro: int, db: Session = Depends(get_db)):
    livro = LivroService.buscar_livro(db, id_livro)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro


@router.get("/", response_model=list[LivroResponse])
def listar_livros(db: Session = Depends(get_db)):
    return LivroService.listar_livros(db)
