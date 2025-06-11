from datetime import datetime
from typing import List

from sqlmodel import Session, and_, select

from crud.base import CRUDBase
from config.logging_config import log_operation
from domain.models import (
    Emprestimo,
    EmprestimoCreate,
    EmprestimoUpdate,
    LivroEmprestimoLink,
    StatusEmprestimo,
)


class CRUDEmprestimo(CRUDBase[Emprestimo, EmprestimoCreate, EmprestimoUpdate]):
    def create_with_livros(
        self, db: Session, *, obj_in: EmprestimoCreate
    ) -> Emprestimo:
        """Criar empréstimo com livros associados"""
        try:
            # Criar empréstimo
            obj_data = obj_in.model_dump(exclude={"livro_ids"})
            db_obj = Emprestimo(**obj_data)
            db.add(db_obj)
            db.flush()  # Para obter o ID sem fazer commit

            # Associar livros
            for livro_id in obj_in.livro_ids:
                link = LivroEmprestimoLink(livro_id=livro_id, emprestimo_id=db_obj.id)
                db.add(link)

            db.commit()
            db.refresh(db_obj)
            log_operation("CREATE_WITH_LIVROS", "Emprestimo", db_obj.id, True)
            return db_obj
        except Exception as e:
            db.rollback()
            log_operation("CREATE_WITH_LIVROS", "Emprestimo", None, False, str(e))
            raise

    def get_by_usuario(self, db: Session, *, usuario_id: int) -> List[Emprestimo]:
        """Filtrar empréstimos por usuário"""
        statement = select(Emprestimo).where(Emprestimo.usuario_id == usuario_id)
        return db.exec(statement).all()

    def get_by_status(
        self, db: Session, *, status: StatusEmprestimo
    ) -> List[Emprestimo]:
        """Filtrar por status"""
        statement = select(Emprestimo).where(Emprestimo.status == status)
        return db.exec(statement).all()

    def get_atrasados(self, db: Session) -> List[Emprestimo]:
        """Listar empréstimos atrasados"""
        hoje = datetime.now()
        statement = select(Emprestimo).where(
            and_(
                Emprestimo.status == StatusEmprestimo.ATIVO,
                Emprestimo.data_devolucao_prevista < hoje,
            )
        )
        return db.exec(statement).all()

    def get_with_livros(self, db: Session, emprestimo_id: int) -> Emprestimo:
        """Buscar empréstimo com livros associados"""
        statement = select(Emprestimo).where(Emprestimo.id == emprestimo_id)
        emprestimo = db.exec(statement).first()
        if emprestimo:
            # Força o carregamento dos livros relacionados
            _ = emprestimo.livros
        return emprestimo

    def get_all_with_livros(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[Emprestimo]:
        """Listar empréstimos com livros associados"""
        statement = select(Emprestimo).offset(skip).limit(limit)
        emprestimos = db.exec(statement).all()
        # Força o carregamento dos livros para cada empréstimo
        for emprestimo in emprestimos:
            _ = emprestimo.livros
        return emprestimos


# Instância do CRUD
crud_emprestimo = CRUDEmprestimo(Emprestimo)
