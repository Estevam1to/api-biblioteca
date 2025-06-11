from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config.database import create_db_and_tables
from config.logging_config import setup_logging
from routers import autores, editoras, emprestimos, livros, usuarios

# Configurar logging
logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerenciar ciclo de vida da aplicação"""
    # Startup
    try:
        create_db_and_tables()
        logger.info("Aplicação iniciada com sucesso")
    except Exception as e:
        logger.error(f"Erro na inicialização: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Aplicação finalizada")


app = FastAPI(
    title="API Biblioteca",
    description="Sistema de gerenciamento de biblioteca com ORM",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
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


# Handler global para exceções
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Erro não tratado: {exc}")
    raise HTTPException(status_code=500, detail="Erro interno do servidor")


@app.get("/health")
def health_check():
    """Endpoint de verificação de saúde da API"""
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}


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

    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
