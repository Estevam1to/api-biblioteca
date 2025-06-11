from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.crud import crud_editora
from app.database import get_session
from app.models import EditoraCreate, EditoraRead, EditoraUpdate

router = APIRouter(prefix="/editoras", tags=["editoras"])


@router.post("/", response_model=EditoraRead)
def criar_editora(editora: EditoraCreate, db: Session = Depends(get_session)):
    """Criar uma nova editora"""
    return crud_editora.create(db=db, obj_in=editora)


@router.get("/", response_model=List[EditoraRead])
def listar_editoras(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    nome: Optional[str] = Query(None),
    db: Session = Depends(get_session),
):
    """Listar editoras com filtros opcionais"""
    if nome:
        return crud_editora.get_by_nome(db=db, nome=nome)
    else:
        return crud_editora.get_multi(db=db, skip=skip, limit=limit)


@router.get("/count")
def contar_editoras(db: Session = Depends(get_session)):
    """Contar total de editoras"""
    count = crud_editora.count(db=db)
    return {"quantidade": count}


@router.get("/{editora_id}", response_model=EditoraRead)
def buscar_editora(editora_id: int, db: Session = Depends(get_session)):
    """Buscar editora por ID"""
    editora = crud_editora.get(db=db, id=editora_id)
    if not editora:
        raise HTTPException(status_code=404, detail="Editora não encontrada")
    return editora


@router.put("/{editora_id}", response_model=EditoraRead)
def atualizar_editora(
    editora_id: int, editora_update: EditoraUpdate, db: Session = Depends(get_session)
):
    """Atualizar editora"""
    editora = crud_editora.get(db=db, id=editora_id)
    if not editora:
        raise HTTPException(status_code=404, detail="Editora não encontrada")
    return crud_editora.update(db=db, db_obj=editora, obj_in=editora_update)


@router.delete("/{editora_id}")
def deletar_editora(editora_id: int, db: Session = Depends(get_session)):
    """Deletar editora"""
    editora = crud_editora.remove(db=db, id=editora_id)
    if not editora:
        raise HTTPException(status_code=404, detail="Editora não encontrada")
    return {"message": "Editora deletada com sucesso"}
