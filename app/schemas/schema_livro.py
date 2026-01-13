from pydantic import BaseModel
from typing import Optional
from app.domain.enums.categoria_livro import CategoriaLivro
from app.domain.enums.localizacao_livro import LocalizacaoLivro


class LivroBase(BaseModel):
    titulo: str
    autor: str
    qtd_copias: int
    copias_disponiveis: int


class LivroCreate(LivroBase):
    categoria: CategoriaLivro
    localizacao: LocalizacaoLivro | None = None


class LivroResponse(BaseModel):
    id_livro: int
    titulo: str
    autor: str
    categoria: str
    qtd_copias: int
    copias_disponiveis: int
    localizacao: str | None

    class Config:
        orm_mode = True

