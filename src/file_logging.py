import logging
from pathlib import Path

log_path = Path(__file__).parent.parent.absolute() / "main.log"

logging.basicConfig()
logger = logging.getLogger("main_log")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_path)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.propagate = False
logger.addHandler(file_handler)
