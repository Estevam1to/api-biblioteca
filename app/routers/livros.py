from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.crud import crud_autor, crud_editora, crud_livro
from app.database import get_session
from app.models import LivroCreate, LivroRead, LivroUpdate

router = APIRouter(prefix="/livros", tags=["livros"])


@router.post("/", response_model=LivroRead)
def criar_livro(livro: LivroCreate, db: Session = Depends(get_session)):
    """Criar um novo livro"""
    # Verificar se autor existe
    autor = crud_autor.get(db=db, id=livro.autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor não encontrado")

    # Verificar se editora existe
    editora = crud_editora.get(db=db, id=livro.editora_id)
    if not editora:
        raise HTTPException(status_code=404, detail="Editora não encontrada")

    return crud_livro.create(db=db, obj_in=livro)


@router.get("/", response_model=List[LivroRead])
def listar_livros(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    titulo: Optional[str] = Query(None),
    genero: Optional[str] = Query(None),
    autor_id: Optional[int] = Query(None),
    ano_inicio: Optional[int] = Query(None),
    ano_fim: Optional[int] = Query(None),
    db: Session = Depends(get_session),
):
    """Listar livros com filtros avançados"""
    if titulo:
        return crud_livro.get_by_titulo(db=db, titulo=titulo)
    elif genero:
        return crud_livro.get_by_genero(db=db, genero=genero)
    elif autor_id:
        return crud_livro.get_by_autor(db=db, autor_id=autor_id)
    elif ano_inicio:
        return crud_livro.get_by_ano(db=db, ano_inicio=ano_inicio, ano_fim=ano_fim)
    else:
        return crud_livro.get_multi(db=db, skip=skip, limit=limit)


@router.get("/count")
def contar_livros(db: Session = Depends(get_session)):
    """Contar total de livros"""
    count = crud_livro.count(db=db)
    return {"quantidade": count}


@router.get("/{livro_id}", response_model=LivroRead)
def buscar_livro(livro_id: int, db: Session = Depends(get_session)):
    """Buscar livro por ID"""
    livro = crud_livro.get(db=db, id=livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro


@router.put("/{livro_id}", response_model=LivroRead)
def atualizar_livro(
    livro_id: int, livro_update: LivroUpdate, db: Session = Depends(get_session)
):
    """Atualizar livro"""
    livro = crud_livro.get(db=db, id=livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    # Verificar se novos IDs existem
    if livro_update.autor_id:
        autor = crud_autor.get(db=db, id=livro_update.autor_id)
        if not autor:
            raise HTTPException(status_code=404, detail="Autor não encontrado")

    if livro_update.editora_id:
        editora = crud_editora.get(db=db, id=livro_update.editora_id)
        if not editora:
            raise HTTPException(status_code=404, detail="Editora não encontrada")

    return crud_livro.update(db=db, db_obj=livro, obj_in=livro_update)


@router.delete("/{livro_id}")
def deletar_livro(livro_id: int, db: Session = Depends(get_session)):
    """Deletar livro"""
    livro = crud_livro.remove(db=db, id=livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return {"message": "Livro deletado com sucesso"}
