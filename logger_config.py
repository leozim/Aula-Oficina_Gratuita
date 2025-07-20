
import logging
import sys


def setup_logger():
    logger = logging.getLogger("AppAulasGratuitas")

    # Previne a adição de múltiplos handlers se a função for chamada mais de uma vez
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)

    return logger


# Cria uma instância única do logger para ser importada por outros módulos
log = setup_logger()