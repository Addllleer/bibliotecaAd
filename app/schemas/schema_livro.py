from pydantic import BaseModel
from typing import Optional


class LivroBase(BaseModel):
    titulo: str
    autor: str
    categoria: str
    qtd_copias: int
    copias_disponiveis: int
    localizacao: Optional[str] = None


class LivroCreate(LivroBase):
    pass


class LivroResponse(LivroBase):
    id_livro: int

    class Config:
        orm_mode = True
