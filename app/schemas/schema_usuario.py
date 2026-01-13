from pydantic import BaseModel
from typing import List, Optional
from app.domain.enums.perfil_acesso import PerfilAcesso

class UsuarioBase(BaseModel):
    nome: str
    perfil_acesso: PerfilAcesso

class UsuarioCreate(UsuarioBase):
    pass


class UsuarioResponse(UsuarioBase):
    id_usuario: int

    class Config:
        orm_mode = True
