"""
This file is only used in "test_logging_wrappers".
"""

from logging import Logger
from ..logging_wrappers import getLogger

logger: Logger = getLogger()


def raise_zero_div():
    logger.error("zero div", stack_info=True)
    1 / 0
