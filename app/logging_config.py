import logging
import os
from app.config import settings

def setup_logging():
    """Configura o sistema de logging"""
    
    # Criar diretório de logs se não existir
    log_dir = os.path.dirname(settings.log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configurar formatação
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Handler para arquivo
    file_handler = logging.FileHandler(settings.log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(getattr(logging, settings.log_level))
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    
    # Configurar logger raiz
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.log_level))
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Logger específico para a aplicação
    app_logger = logging.getLogger("biblioteca_api")
    app_logger.info("Sistema de logging configurado")
    
    return app_logger

# Criar logger global
logger = setup_logging()

def log_operation(operation: str, entity: str, entity_id: int = None, success: bool = True, error: str = None):
    """Registra operações realizadas na API"""
    if success:
        msg = f"Operação {operation} realizada com sucesso na entidade {entity}"
        if entity_id:
            msg += f" (ID: {entity_id})"
        logger.info(msg)
    else:
        msg = f"Erro na operação {operation} na entidade {entity}"
        if entity_id:
            msg += f" (ID: {entity_id})"
        if error:
            msg += f" - Erro: {error}"
        logger.error(msg)
