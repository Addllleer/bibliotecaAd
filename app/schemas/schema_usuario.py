from pydantic import BaseModel
from typing import List, Optional


class UsuarioBase(BaseModel):
    nome: str
    perfil_acesso: str


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioResponse(UsuarioBase):
    id_usuario: int

    class Config:
        orm_mode = True
