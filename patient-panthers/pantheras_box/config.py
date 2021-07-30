import logging
from pathlib import Path

SCORE_FILE = Path(__file__).parent.absolute() / "high_score.yaml"
LOG_FILE = Path(__file__).parent.absolute() / "main.log"

LOG_LEVEL = logging.INFO
