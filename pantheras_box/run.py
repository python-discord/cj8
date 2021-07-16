import argparse
import logging
import sys
from typing import NoReturn

from pantheras_box import config
from pantheras_box.frontend.core import CoreFrontend


def run_game() -> NoReturn:
    """Run the game."""
    parser = argparse.ArgumentParser(prog="Panthera's Box")
    parser.add_argument("-t", "--testing", action="store_true")
    parser.add_argument("--flush-score", action="store_true")
    parser.add_argument("--flush-log", action="store_true")

    cli_args = vars(parser.parse_args())

    score_flush = cli_args.pop("flush_score")
    log_flush = cli_args.pop("flush_log")

    if score_flush:
        score_file = config.SCORE_FILE
        score_file.unlink(missing_ok=True)

    if log_flush:
        logging.shutdown()
        log_file = config.LOG_FILE
        log_file.unlink()

    frontend = CoreFrontend(cli_args)
    try:
        frontend.start_loop()
    except KeyboardInterrupt:
        logging.shutdown()
        sys.exit(0)
