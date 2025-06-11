import logging

from sqlmodel import Session, SQLModel, create_engine

from app.config.config import settings

logger = logging.getLogger(__name__)

engine = create_engine(
    settings.database_url,
    echo=False,
    pool_pre_ping=True
)

def create_db_and_tables():
    """Cria as tabelas no banco de dados"""
    try:
        SQLModel.metadata.create_all(engine)
        logger.info("Tabelas criadas com sucesso")
    except Exception as e:
        logger.error(f"Erro ao criar tabelas: {e}")
        raise

def get_session():
    """Dependency para obter sessão do banco"""
    with Session(engine) as session:
        yield session
