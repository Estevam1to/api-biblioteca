from typing import List

from sqlmodel import Session, select

from crud.base import CRUDBase
from app.domain.models import Editora, EditoraCreate, EditoraUpdate


class CRUDEditora(CRUDBase[Editora, EditoraCreate, EditoraUpdate]):
    def get_by_nome(self, db: Session, *, nome: str) -> List[Editora]:
        """Buscar editoras por nome (busca parcial)"""
        statement = select(Editora).where(Editora.nome.ilike(f"%{nome}%"))
        return db.exec(statement).all()


# Instância do CRUD
crud_editora = CRUDEditora(Editora)
