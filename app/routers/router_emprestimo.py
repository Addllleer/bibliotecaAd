from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.schema_emprestimo import EmprestimoCreate, EmprestimoResponse
from app.services.service_emprestimo import EmprestimoService

router = APIRouter(prefix="/emprestimos", tags=["Empréstimos"])


@router.post("/", response_model=EmprestimoResponse, status_code=status.HTTP_201_CREATED)
def realizar_emprestimo(dados: EmprestimoCreate, db: Session = Depends(get_db)):
    try:
        return EmprestimoService.realizar_emprestimo(
            db=db,
            id_usuario=dados.id_usuario,
            id_livro=dados.id_livro
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{id_emprestimo}/devolucao", response_model=EmprestimoResponse)
def devolver_livro(id_emprestimo: int, db: Session = Depends(get_db)):
    try:
        return EmprestimoService.devolver_livro(db, id_emprestimo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
