from pydantic import BaseModel
from datetime import date
from typing import Optional


class EmprestimoBase(BaseModel):
    id_usuario: int
    id_livro: int


class EmprestimoCreate(EmprestimoBase):
    pass


class EmprestimoResponse(EmprestimoBase):
    id_emprestimo: int
    data_emprestimo: date
    prazo_devolucao: date
    data_devolucao: Optional[date]
    multa: Optional[float]
    status: str

    class Config:
        orm_mode = True
