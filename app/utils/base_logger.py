import logging

logger = logging
logger.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%d.%m | %H:%M:%S",
    level=logging.INFO,
)
