from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

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
    responses={
        201: {"description": "Usuário criado com sucesso"},
        400: {"description": "Usuário já existe"}
    }
)
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


@router.get(
    "/{id_usuario}",
    response_model=UsuarioResponse,
    summary="Buscar usuário por ID",
    description="Retorna os dados de um usuário a partir do seu identificador.",
    responses={
        200: {"description": "Usuário encontrado"},
        404: {"description": "Usuário não encontrado"}
    }
)
def buscar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    usuario = UsuarioService.buscar_usuario(db, id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario


@router.get(
    "/",
    response_model=list[UsuarioResponse],
    summary="Listar usuários",
    description="Lista usuários cadastrados no sistema com paginação.",
    responses={
        200: {"description": "Lista de usuários retornada com sucesso"}
    }
)
def listar_usuarios(
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(10, ge=1, le=100, description="Quantidade de registros por página"),
    db: Session = Depends(get_db)
):
    return UsuarioService.listar_usuarios(db, page, size)
