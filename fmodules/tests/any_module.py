"""
This file is only used in "test_logging_wrappers".
"""

from logging import Logger
from ..logging_wrappers import getLogger

logger: Logger = getLogger()


def log(msg: str):
    logger.info(msg)
