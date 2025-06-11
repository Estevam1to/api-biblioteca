from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import create_db_and_tables
from app.logging_config import setup_logging
from app.routers import autores, editoras, emprestimos, livros, usuarios

logger = setup_logging()

app = FastAPI(
    title="API Biblioteca",
    description="Sistema de gerenciamento de biblioteca com ORM",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(autores.router)
app.include_router(editoras.router)
app.include_router(livros.router)
app.include_router(usuarios.router)
app.include_router(emprestimos.router)


@app.on_event("startup")
def on_startup():
    """Executado na inicialização da aplicação"""
    try:
        create_db_and_tables()
        logger.info("Aplicação iniciada com sucesso")
    except Exception as e:
        logger.error(f"Erro na inicialização: {e}")
        raise


@app.get("/")
def root():
    """Endpoint raiz da API"""
    return {
        "message": "API Biblioteca - Sistema de Gerenciamento",
        "version": "1.0.0",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=5000)
