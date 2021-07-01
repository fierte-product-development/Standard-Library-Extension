import pytest
from pathlib import Path
import re
from ..logging_wrappers import getLogger

from . import any_module


class Test_getLogger:
    def test_LoggersInOtherModulesWillLogWithMyName_PassedTrueToRoot(self, capfd):
        getLogger(root=True)
        any_module.log("test")
        out, _ = capfd.readouterr()
        assert re.search(r"\[" + Path(__file__).stem + r"\." + "any_module" + r"\]", out)

    def test_LoggersInOtherModulesWillLogWithRootName_PassedRootAndName(self, capfd):
        root_name = "hoge"
        getLogger(root=True, name=root_name)
        any_module.log("test")
        out, _ = capfd.readouterr()
        assert re.search(r"\[" + root_name + r"\." + "any_module" + r"\]", out)
