from pydantic import BaseModel, Field
from app.domain.enums.perfil_acesso import PerfilAcesso
from typing import List
from app.schemas.schema_emprestimo import EmprestimoResumoResponse



class UsuarioBase(BaseModel):
    nome: str


class UsuarioCreate(UsuarioBase):
    perfil_acesso: PerfilAcesso


class UsuarioResponse(UsuarioBase):
    id_usuario: int
    perfil_acesso: str 
    emprestimos: List[EmprestimoResumoResponse] = []

    class Config:
        orm_mode = True

class UsuarioCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    perfil_acesso: PerfilAcesso