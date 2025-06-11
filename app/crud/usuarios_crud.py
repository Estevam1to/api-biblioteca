from typing import List, Optional

from sqlmodel import Session, select

from app.crud.base import CRUDBase
from app.models import Usuario, UsuarioCreate, UsuarioUpdate


class CRUDUsuario(CRUDBase[Usuario, UsuarioCreate, UsuarioUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Usuario]:
        """Buscar usuário por email"""
        statement = select(Usuario).where(Usuario.email == email)
        return db.exec(statement).first()

    def get_by_cpf(self, db: Session, *, cpf: str) -> Optional[Usuario]:
        """Buscar usuário por CPF"""
        statement = select(Usuario).where(Usuario.cpf == cpf)
        return db.exec(statement).first()

    def get_ativos(self, db: Session) -> List[Usuario]:
        """Listar apenas usuários ativos"""
        statement = select(Usuario).where(Usuario.ativo is True)
        return db.exec(statement).all()



crud_usuario = CRUDUsuario(Usuario)
