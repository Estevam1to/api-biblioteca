from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.crud import crud_emprestimo, crud_livro, crud_usuario
from app.database import get_session
from app.models import (
    EmprestimoCreate,
    EmprestimoRead,
    EmprestimoUpdate,
    StatusEmprestimo,
)

router = APIRouter(prefix="/emprestimos", tags=["emprestimos"])


@router.post("/", response_model=EmprestimoRead)
def criar_emprestimo(emprestimo: EmprestimoCreate, db: Session = Depends(get_session)):
    """Criar um novo empréstimo"""
    # Verificar se usuário existe
    usuario = crud_usuario.get(db=db, id=emprestimo.usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Verificar se todos os livros existem
    for livro_id in emprestimo.livro_ids:
        livro = crud_livro.get(db=db, id=livro_id)
        if not livro:
            raise HTTPException(
                status_code=404, detail=f"Livro {livro_id} não encontrado"
            )

    return crud_emprestimo.create_with_livros(db=db, obj_in=emprestimo)


@router.get("/", response_model=List[EmprestimoRead])
def listar_emprestimos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    usuario_id: Optional[int] = Query(None),
    status: Optional[StatusEmprestimo] = Query(None),
    atrasados: bool = Query(False),
    db: Session = Depends(get_session),
):
    """Listar empréstimos com filtros opcionais"""
    if atrasados:
        return crud_emprestimo.get_atrasados(db=db)
    elif usuario_id:
        return crud_emprestimo.get_by_usuario(db=db, usuario_id=usuario_id)
    elif status:
        return crud_emprestimo.get_by_status(db=db, status=status)
    else:
        return crud_emprestimo.get_multi(db=db, skip=skip, limit=limit)


@router.get("/count")
def contar_emprestimos(db: Session = Depends(get_session)):
    """Contar total de empréstimos"""
    count = crud_emprestimo.count(db=db)
    return {"quantidade": count}


@router.get("/{emprestimo_id}", response_model=EmprestimoRead)
def buscar_emprestimo(emprestimo_id: int, db: Session = Depends(get_session)):
    """Buscar empréstimo por ID"""
    emprestimo = crud_emprestimo.get(db=db, id=emprestimo_id)
    if not emprestimo:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
    return emprestimo


@router.put("/{emprestimo_id}", response_model=EmprestimoRead)
def atualizar_emprestimo(
    emprestimo_id: int,
    emprestimo_update: EmprestimoUpdate,
    db: Session = Depends(get_session),
):
    """Atualizar empréstimo"""
    emprestimo = crud_emprestimo.get(db=db, id=emprestimo_id)
    if not emprestimo:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")

    return crud_emprestimo.update(db=db, db_obj=emprestimo, obj_in=emprestimo_update)


@router.put("/{emprestimo_id}/devolver")
def devolver_emprestimo(emprestimo_id: int, db: Session = Depends(get_session)):
    """Marcar empréstimo como devolvido"""
    emprestimo = crud_emprestimo.get(db=db, id=emprestimo_id)
    if not emprestimo:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")

    if emprestimo.status == StatusEmprestimo.DEVOLVIDO:
        raise HTTPException(status_code=400, detail="Empréstimo já foi devolvido")

    update_data = EmprestimoUpdate(
        status=StatusEmprestimo.DEVOLVIDO, data_devolucao_real=datetime.now()
    )

    updated_emprestimo = crud_emprestimo.update(
        db=db, db_obj=emprestimo, obj_in=update_data
    )
    return {
        "message": "Empréstimo devolvido com sucesso",
        "emprestimo": updated_emprestimo,
    }


@router.delete("/{emprestimo_id}")
def deletar_emprestimo(emprestimo_id: int, db: Session = Depends(get_session)):
    """Deletar empréstimo"""
    emprestimo = crud_emprestimo.remove(db=db, id=emprestimo_id)
    if not emprestimo:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
    return {"message": "Empréstimo deletado com sucesso"}
