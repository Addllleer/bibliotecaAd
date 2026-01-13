from pydantic import BaseModel
from typing import Optional
from app.domain.enums.categoria_livro import CategoriaLivro
from app.domain.enums.localizacao_livro import LocalizacaoLivro


class LivroBase(BaseModel):
    titulo: str
    autor: str
    categoria: CategoriaLivro
    qtd_copias: int
    copias_disponiveis: int
    localizacao: LocalizacaoLivro | None = None


class LivroCreate(LivroBase):
    pass


class LivroResponse(LivroBase):
    id_livro: int

    class Config:
        orm_mode = True
