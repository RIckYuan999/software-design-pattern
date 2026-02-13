from __future__ import annotations

import logging
import sys

_configured = False


def _configure_root_logger() -> None:
    global _configured
    if _configured:
        return

    root_logger = logging.getLogger()
    
    if root_logger.hasHandlers():
        return

    root_logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s",
        datefmt="%H:%M:%S"
    )
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    _configured = True


def get_logger(name: str) -> logging.Logger:

    _configure_root_logger()
    return logging.getLogger(name)


setup_logger = get_logger
