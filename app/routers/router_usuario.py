from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.schema_usuario import UsuarioCreate, UsuarioResponse
from app.services.service_usuario import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        return UsuarioService.criar_usuario(
            db=db,
            nome=usuario.nome,
            perfil_acesso=usuario.perfil_acesso
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{id_usuario}", response_model=UsuarioResponse)
def buscar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    usuario = UsuarioService.buscar_usuario(db, id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return UsuarioService.listar_usuarios(db)
