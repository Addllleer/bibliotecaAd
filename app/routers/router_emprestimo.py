from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.schema_emprestimo import EmprestimoCreate, EmprestimoResponse
from app.services.service_emprestimo import EmprestimoService

router = APIRouter(prefix="/emprestimos", tags=["Empréstimos"])


@router.post(
    "/",
    response_model=EmprestimoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Realizar empréstimo",
    description="Realiza o empréstimo de um livro para um usuário.",
    responses={
        201: {"description": "Empréstimo realizado com sucesso"},
        400: {"description": "Regra de negócio violada"}
    }
)
def realizar_emprestimo(dados: EmprestimoCreate, db: Session = Depends(get_db)):
    try:
        return EmprestimoService.realizar_emprestimo(
            db=db,
            id_usuario=dados.id_usuario,
            id_livro=dados.id_livro,
            data_emprestimo=dados.data_emprestimo
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/{id_emprestimo}/devolucao",
    response_model=EmprestimoResponse,
    summary="Devolver livro",
    description="Realiza a devolução de um empréstimo e calcula multa, se houver.",
    responses={
        200: {"description": "Livro devolvido com sucesso"},
        400: {"description": "Erro ao devolver empréstimo"}
    }
)
def devolver_livro(id_emprestimo: int, db: Session = Depends(get_db)):
    try:
        return EmprestimoService.devolver_livro(db, id_emprestimo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/atuais",
    response_model=list[EmprestimoResponse],
    summary="Listar empréstimos atuais",
    description="Lista empréstimos com status ATIVO ou ATRASADO, com paginação.",
    responses={
        200: {"description": "Lista de empréstimos atuais"}
    }
)
def listar_emprestimos_atuais(
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(10, ge=1, le=100, description="Quantidade de registros por página"),
    db: Session = Depends(get_db)
):
    return EmprestimoService.listar_emprestimos_atuais(db, page, size)


@router.get(
    "/historico",
    response_model=list[EmprestimoResponse],
    summary="Histórico de empréstimos",
    description="Lista todo o histórico de empréstimos, incluindo devolvidos.",
    responses={
        200: {"description": "Histórico completo de empréstimos"}
    }
)
def listar_historico_emprestimos(
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(10, ge=1, le=100, description="Quantidade de registros por página"),
    db: Session = Depends(get_db)
):
    return EmprestimoService.listar_historico_emprestimos(db, page, size)
