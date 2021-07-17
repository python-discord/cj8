import argparse
import logging
from typing import Optional

from pantheras_box import config
from pantheras_box.backend.core import CoreBackend

_backend_singleton: Optional[CoreBackend] = None


def get_singleton() -> CoreBackend:
    """Singleton implementation for the backend"""
    parser = argparse.ArgumentParser(prog="Panthera's Box")
    parser.add_argument("-t", "--testing", action="store_true")
    parser.add_argument("--flush-score", action="store_true")
    parser.add_argument("--flush-log", action="store_true")

    cli_args = vars(parser.parse_args())

    score_flush = cli_args.pop("flush_score")
    log_flush = cli_args.pop("flush_log")

    print(cli_args)

    if score_flush:
        score_file = config.SCORE_FILE
        score_file.unlink(missing_ok=True)

    if log_flush:
        logging.shutdown()
        log_file = config.LOG_FILE
        log_file.unlink()

    global _backend_singleton
    if not _backend_singleton:
        _backend_singleton = CoreBackend(cli_args)

    return _backend_singleton
