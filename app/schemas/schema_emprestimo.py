from pydantic import BaseModel
from datetime import date
from typing import Optional


class EmprestimoBase(BaseModel):
    id_usuario: int
    id_livro: int


class EmprestimoCreate(EmprestimoBase):
    data_emprestimo: Optional[date] = None


class EmprestimoResponse(EmprestimoBase):
    id_emprestimo: int
    data_emprestimo: date
    prazo_devolucao: date
    data_devolucao: Optional[date]
    multa: Optional[float]
    status: str

    class Config:
        orm_mode = True

class EmprestimoResumoResponse(BaseModel):
    id_emprestimo: int
    id_livro: int
    status: str
    data_emprestimo: date
    prazo_devolucao: date
    data_devolucao: Optional[date]
    multa: Optional[float]

    class Config:
        from_attributes = True
