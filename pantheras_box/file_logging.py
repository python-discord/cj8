import logging

from pantheras_box.config import LOG_FILE, LOG_LEVEL

log_path = LOG_FILE
logging.basicConfig()
logger = logging.getLogger("main_log")
logger.setLevel(LOG_LEVEL)
file_handler = logging.FileHandler(log_path)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.propagate = False
logger.addHandler(file_handler)
