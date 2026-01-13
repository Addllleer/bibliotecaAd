from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.schema_livro import LivroCreate, LivroResponse
from app.services.service_livro import LivroService

router = APIRouter(prefix="/livros", tags=["Livros"])


@router.post(
    "/",
    response_model=LivroResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar livro",
    description="Cadastra um novo livro na biblioteca.",
    responses={
        201: {"description": "Livro cadastrado com sucesso"},
        400: {"description": "Erro de validação"}
    }
)
def criar_livro(livro: LivroCreate, db: Session = Depends(get_db)):
    return LivroService.criar_livro(
        db=db,
        titulo=livro.titulo,
        autor=livro.autor,
        categoria=livro.categoria,
        qtd_copias=livro.qtd_copias,
        localizacao=livro.localizacao
    )


@router.get(
    "/{id_livro}",
    response_model=LivroResponse,
    summary="Buscar livro por ID",
    description="Retorna os dados de um livro a partir do seu identificador.",
    responses={
        200: {"description": "Livro encontrado"},
        404: {"description": "Livro não encontrado"}
    }
)
def buscar_livro(id_livro: int, db: Session = Depends(get_db)):
    livro = LivroService.buscar_livro(db, id_livro)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro


@router.get(
    "/",
    response_model=list[LivroResponse],
    summary="Listar livros",
    description="Lista os livros cadastrados na biblioteca com paginação.",
    responses={
        200: {"description": "Lista de livros retornada com sucesso"}
    }
)
def listar_livros(
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(10, ge=1, le=100, description="Quantidade de registros por página"),
    db: Session = Depends(get_db)
):
    return LivroService.listar_livros(db, page, size)
