import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
log_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('../logs/logs.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)
