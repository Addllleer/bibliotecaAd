from pydantic import BaseModel
from app.domain.enums.perfil_acesso import PerfilAcesso


class UsuarioBase(BaseModel):
    nome: str


class UsuarioCreate(UsuarioBase):
    perfil_acesso: PerfilAcesso


class UsuarioResponse(UsuarioBase):
    id_usuario: int
    perfil_acesso: str 

    class Config:
        orm_mode = True
