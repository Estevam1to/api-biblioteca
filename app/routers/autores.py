from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from crud.autores_crud import crud_autor
from app.config.database import get_session
from app.domain.models import AutorCreate, AutorRead, AutorUpdate

router = APIRouter(prefix="/autores", tags=["autores"])


@router.post("/", response_model=AutorRead)
def criar_autor(autor: AutorCreate, db: Session = Depends(get_session)):
    """Criar um novo autor"""
    return crud_autor.create(db=db, obj_in=autor)


@router.get("/", response_model=List[AutorRead])
def listar_autores(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    nome: Optional[str] = Query(None),
    nacionalidade: Optional[str] = Query(None),
    db: Session = Depends(get_session),
):
    """Listar autores com filtros opcionais"""
    if nome:
        return crud_autor.get_by_nome(db=db, nome=nome)
    elif nacionalidade:
        return crud_autor.get_by_nacionalidade(db=db, nacionalidade=nacionalidade)
    else:
        return crud_autor.get_multi(db=db, skip=skip, limit=limit)


@router.get("/count")
def contar_autores(db: Session = Depends(get_session)):
    """Contar total de autores"""
    count = crud_autor.count(db=db)
    return {"quantidade": count}


@router.get("/{autor_id}", response_model=AutorRead)
def buscar_autor(autor_id: int, db: Session = Depends(get_session)):
    """Buscar autor por ID"""
    autor = crud_autor.get(db=db, id=autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    return autor


@router.put("/{autor_id}", response_model=AutorRead)
def atualizar_autor(
    autor_id: int, autor_update: AutorUpdate, db: Session = Depends(get_session)
):
    """Atualizar autor"""
    autor = crud_autor.get(db=db, id=autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    return crud_autor.update(db=db, db_obj=autor, obj_in=autor_update)


@router.delete("/{autor_id}")
def deletar_autor(autor_id: int, db: Session = Depends(get_session)):
    """Deletar autor"""
    autor = crud_autor.remove(db=db, id=autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    return {"message": "Autor deletado com sucesso"}
