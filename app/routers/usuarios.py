from typing import List

from crud.usuarios_crud import crud_usuario
from app.config.database import get_session
from fastapi import APIRouter, Depends, HTTPException, Query
from app.domain.models import UsuarioCreate, UsuarioRead, UsuarioUpdate
from sqlmodel import Session

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.post("/", response_model=UsuarioRead)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_session)):
    """Criar um novo usuário"""
    existing_user = crud_usuario.get_by_email(db=db, email=usuario.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    existing_cpf = crud_usuario.get_by_cpf(db=db, cpf=usuario.cpf)
    if existing_cpf:
        raise HTTPException(status_code=400, detail="CPF já cadastrado")

    return crud_usuario.create(db=db, obj_in=usuario)


@router.get("/", response_model=List[UsuarioRead])
def listar_usuarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    apenas_ativos: bool = Query(False),
    db: Session = Depends(get_session),
):
    """Listar usuários com filtros opcionais"""
    if apenas_ativos:
        return crud_usuario.get_ativos(db=db)
    else:
        return crud_usuario.get_multi(db=db, skip=skip, limit=limit)


@router.get("/count")
def contar_usuarios(db: Session = Depends(get_session)):
    """Contar total de usuários"""
    count = crud_usuario.count(db=db)
    return {"quantidade": count}


@router.get("/email/{email}", response_model=UsuarioRead)
def buscar_por_email(email: str, db: Session = Depends(get_session)):
    """Buscar usuário por email"""
    usuario = crud_usuario.get_by_email(db=db, email=email)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario


@router.get("/{usuario_id}", response_model=UsuarioRead)
def buscar_usuario(usuario_id: int, db: Session = Depends(get_session)):
    """Buscar usuário por ID"""
    usuario = crud_usuario.get(db=db, id=usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario


@router.put("/{usuario_id}", response_model=UsuarioRead)
def atualizar_usuario(
    usuario_id: int, usuario_update: UsuarioUpdate, db: Session = Depends(get_session)
):
    """Atualizar usuário"""
    usuario = crud_usuario.get(db=db, id=usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if usuario_update.email and usuario_update.email != usuario.email:
        existing_user = crud_usuario.get_by_email(db=db, email=usuario_update.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email já cadastrado")

    if usuario_update.cpf and usuario_update.cpf != usuario.cpf:
        existing_cpf = crud_usuario.get_by_cpf(db=db, cpf=usuario_update.cpf)
        if existing_cpf:
            raise HTTPException(status_code=400, detail="CPF já cadastrado")

    return crud_usuario.update(db=db, db_obj=usuario, obj_in=usuario_update)


@router.delete("/{usuario_id}")
def deletar_usuario(usuario_id: int, db: Session = Depends(get_session)):
    """Deletar usuário"""
    usuario = crud_usuario.remove(db=db, id=usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"message": "Usuário deletado com sucesso"}
