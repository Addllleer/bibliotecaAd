from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, Query, HTTPException
from app.database import get_db
from app.schemas.schema_usuario import UsuarioCreate, UsuarioResponse
from app.services.service_usuario import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.post(
    "/",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar usuário",
    description="Cria um novo usuário no sistema. O nome do usuário deve ser único.",
)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return UsuarioService.criar_usuario(
        db=db,
        nome=usuario.nome,
        perfil_acesso=usuario.perfil_acesso
    )


@router.get(
    "/{id_usuario}",
    response_model=UsuarioResponse,
    summary="Buscar usuário por ID",
)
def buscar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    usuario = UsuarioService.buscar_usuario(db, id_usuario)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    return usuario

@router.get(
    "/",
    response_model=list[UsuarioResponse],
    summary="Listar usuários",
)
def listar_usuarios(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return UsuarioService.listar_usuarios(db, page, size)
