import pytest
from typing import Optional
from logging import Logger, FileHandler
from pathlib import Path
from ..logging_wrappers import getLogger

from . import any_module


class Test_getLogger:
    def FindFileHandler(self, l: Logger) -> Optional[FileHandler]:
        for h in l.handlers:
            if isinstance(h, FileHandler):
                return h

    @pytest.mark.order(1)
    def test_SettingsOfChildLoggerWillNotChange_RootIsFalse(self):
        my_logger = getLogger("parent_a", Path("a"))
        assert self.FindFileHandler(my_logger)
        assert not self.FindFileHandler(any_module.logger)

    @pytest.mark.order(2)
    def test_SettingsOfChildLoggerWillChange_RootIsTrue(self):
        my_logger = getLogger("parent_b", Path("b"), root=True)
        assert self.FindFileHandler(my_logger)
        assert self.FindFileHandler(any_module.logger)
