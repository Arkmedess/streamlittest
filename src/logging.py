"""Simple application logging wrapper.

Provides a configured logger with file rotation and helpers to read recent log
lines for display in the Streamlit front-end. Kept intentionally small and
dependency-free.
"""
from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import List

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"


def setup_logger(name: str = "tpi") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    fh = RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=3, encoding="utf-8")
    fh.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s %(levelname)-7s %(name)s %(message)s")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    # console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    # avoid propagation to root
    logger.propagate = False
    return logger


def tail_lines(n: int = 200) -> List[str]:
    """Return the last n lines from the application log as a list.

    If the log file does not exist return an empty list.
    """
    if not LOG_FILE.exists():
        return []

    with LOG_FILE.open("r", encoding="utf-8", errors="ignore") as fh:
        try:
            lines = fh.readlines()
        except Exception:
            return []

    return [l.rstrip("\n") for l in lines[-n:]]
