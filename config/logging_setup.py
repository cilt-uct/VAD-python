import logging
from .config import LOGS

logger = logging.getLogger()
logger.setLevel(logging.INFO)
log_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler(LOGS)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)
