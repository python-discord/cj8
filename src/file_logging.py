import logging

logging.basicConfig()
logger = logging.getLogger("main_log")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("game.log")
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.propagate = False
logger.addHandler(file_handler)
