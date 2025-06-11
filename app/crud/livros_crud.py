from typing import List

from sqlmodel import Session, and_, select

from crud.base import CRUDBase
from app.domain.models import Livro, LivroCreate, LivroUpdate


class CRUDLivro(CRUDBase[Livro, LivroCreate, LivroUpdate]):
    def get_by_titulo(self, db: Session, *, titulo: str) -> List[Livro]:
        """Buscar livros por título (busca parcial)"""
        statement = select(Livro).where(Livro.titulo.ilike(f"%{titulo}%"))
        return db.exec(statement).all()

    def get_by_genero(self, db: Session, *, genero: str) -> List[Livro]:
        """Filtrar por gênero"""
        statement = select(Livro).where(Livro.genero == genero)
        return db.exec(statement).all()

    def get_by_ano(
        self, db: Session, *, ano_inicio: int, ano_fim: int = None
    ) -> List[Livro]:
        """Filtrar por ano de publicação"""
        if ano_fim is None:
            ano_fim = ano_inicio
        statement = select(Livro).where(
            and_(Livro.ano_publicacao >= ano_inicio, Livro.ano_publicacao <= ano_fim)
        )
        return db.exec(statement).all()

    def get_by_autor(self, db: Session, *, autor_id: int) -> List[Livro]:
        """Filtrar livros por autor"""
        statement = select(Livro).where(Livro.autor_id == autor_id)
        return db.exec(statement).all()


# Instância do CRUD
crud_livro = CRUDLivro(Livro)
