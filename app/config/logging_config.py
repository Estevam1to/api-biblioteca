import logging
import os

from config.config import settings


def setup_logging():
    """Configura o sistema de logging"""

    log_dir = os.path.dirname(settings.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler = logging.FileHandler(settings.LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(getattr(logging, settings.LOG_LEVEL))

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    app_logger = logging.getLogger("biblioteca_api")
    app_logger.info("Sistema de logging configurado")

    return app_logger


# Criar logger global
logger = setup_logging()


def log_operation(
    operation: str,
    entity: str,
    entity_id: int = None,
    success: bool = True,
    error: str = None,
):
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
