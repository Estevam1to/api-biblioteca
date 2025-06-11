from typing import List

from sqlmodel import Session, select

from crud.base import CRUDBase
from app.domain.models import Autor, AutorCreate, AutorUpdate


class CRUDAutor(CRUDBase[Autor, AutorCreate, AutorUpdate]):
    def get_by_nome(self, db: Session, *, nome: str) -> List[Autor]:
        """Buscar autores por nome (busca parcial)"""
        statement = select(Autor).where(Autor.nome.ilike(f"%{nome}%"))
        return db.exec(statement).all()

    def get_by_nacionalidade(self, db: Session, *, nacionalidade: str) -> List[Autor]:
        """Filtrar por nacionalidade"""
        statement = select(Autor).where(Autor.nacionalidade == nacionalidade)
        return db.exec(statement).all()


crud_autor = CRUDAutor(Autor)
