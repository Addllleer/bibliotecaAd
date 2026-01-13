from pydantic import BaseModel, Field
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

class LivroCreate(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=200)
    autor: str = Field(..., min_length=1, max_length=150)
    categoria: CategoriaLivro
    qtd_copias: int = Field(..., gt=0)
    localizacao: LocalizacaoLivro | None = None
