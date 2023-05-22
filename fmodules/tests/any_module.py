"""
This file is only used in "test_logging_wrappers".
"""

from logging import Logger
from ..logging_wrappers import getLogger

logger: Logger = getLogger()


def debug(msg: str):
    logger.debug(msg)


def info(msg: str):
    logger.info(msg)


def warning(msg: str):
    logger.warning(msg)


def error(msg: str):
    logger.error(msg)


def critical(msg: str):
    logger.critical(msg)
