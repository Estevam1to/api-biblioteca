import logging
from typing import Generic, List, Optional, Type, TypeVar

from sqlmodel import Session, func, select

from config.logging_config import log_operation
from domain.models import SQLModel

logger = logging.getLogger("uvicorn")

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """Criar uma nova entidade"""
        try:
            obj_data = obj_in.model_dump()
            db_obj = self.model(**obj_data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            log_operation("CREATE", self.model.__name__, db_obj.id, True)
            return db_obj
        except Exception as e:
            db.rollback()
            log_operation("CREATE", self.model.__name__, None, False, str(e))
            raise

    def get(self, db: Session, id: int) -> Optional[ModelType]:
        """Buscar por ID"""
        try:
            obj = db.get(self.model, id)
            if obj:
                log_operation("READ", self.model.__name__, id, True)
            return obj
        except Exception as e:
            log_operation("READ", self.model.__name__, id, False, str(e))
            return None

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Listar com paginação"""
        try:
            statement = select(self.model).offset(skip).limit(limit)
            results = db.exec(statement).all()
            log_operation("READ_MULTI", self.model.__name__, None, True)
            return results
        except Exception as e:
            log_operation("READ_MULTI", self.model.__name__, None, False, str(e))
            return []

    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        """Atualizar entidade"""
        try:
            obj_data = obj_in.model_dump(exclude_unset=True)
            for field, value in obj_data.items():
                setattr(db_obj, field, value)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            log_operation("UPDATE", self.model.__name__, db_obj.id, True)
            return db_obj
        except Exception as e:
            db.rollback()
            log_operation("UPDATE", self.model.__name__, db_obj.id, False, str(e))
            raise

    def remove(self, db: Session, *, id: int) -> Optional[ModelType]:
        """Deletar entidade"""
        try:
            obj = db.get(self.model, id)
            if obj:
                db.delete(obj)
                db.commit()
                log_operation("DELETE", self.model.__name__, id, True)
            return obj
        except Exception as e:
            db.rollback()
            log_operation("DELETE", self.model.__name__, id, False, str(e))
            raise

    def count(self, db: Session) -> int:
        """Contar total de registros"""
        try:
            statement = select(func.count(self.model.id))
            count = db.exec(statement).one()
            log_operation("COUNT", self.model.__name__, None, True)
            return count
        except Exception as e:
            log_operation("COUNT", self.model.__name__, None, False, str(e))
            return 0
