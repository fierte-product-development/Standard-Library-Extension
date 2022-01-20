from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL, LogRecord, Formatter
import pytest
from pathlib import Path
from time import strftime, localtime
from ..logging_wrappers import getLogger, fFormatter
from .. import logging_wrappers

from . import any_module, raise_zero_div


@pytest.fixture
def created_time(mocker) -> None:
    # `logging.time.time()` will be assigned to `LogRecord.created` attribute.
    # Therefore, log messages' asctime will be fixed.
    ctime = 1000000000
    mocker.patch("logging.time.time", return_value=ctime)
    return strftime("%Y-%m-%d %X", localtime(ctime))


class Test_fFormatter:
    class Test_format:
        @pytest.fixture
        def fmt(self) -> fFormatter:
            return fFormatter()

        @pytest.mark.parametrize("lv_no, lv_name", [(INFO, "INFO"), (WARNING, "WARNING")])
        def test_OutputMsg_TakesSpecificLevel(self, fmt: fFormatter, created_time, lv_no, lv_name):
            rec = LogRecord("name", lv_no, "pathname", 100, "msg", None, None, func="func")
            assert fmt.format(rec) == f"{lv_name:>8} {created_time} [pathname] msg"

        @pytest.mark.parametrize("lv_no, lv_name", [(DEBUG, "DEBUG"), (ERROR, "ERROR"), (CRITICAL, "CRITICAL")])
        def test_OutputLineNoAndFuncName_TakesSpecificLevel(self, fmt: fFormatter, created_time, lv_no, lv_name):
            rec = LogRecord("name", lv_no, "pathname", 100, "msg", None, None, func="func")
            assert fmt.format(rec) == f"{lv_name:>8} {created_time} [pathname] msg (100:func)"

        def test_OutputStackTrace_SInfoIsStr(self, fmt: fFormatter, created_time):
            rec = LogRecord("name", ERROR, "pathname", 100, "msg", None, None, func="func", sinfo="sinfo")
            assert fmt.format(rec) == f"   ERROR {created_time} [pathname] msg (100:func) \nsinfo"

        def test_OutputRoot_RootIsNotRecModule(self, fmt: fFormatter, created_time, mocker):
            mocker.patch.object(logging_wrappers, "_root", new="_root")
            rec = LogRecord("name", INFO, "pathname", 100, "msg", None, None, func="func")
            assert fmt.format(rec) == f"    INFO {created_time} [_root.pathname] msg"


class Test_getLogger:
    def test_LoggersInOtherModulesWillLogWithMyName_PassedTrueToRoot(self, capfd, created_time):
        getLogger(root=True)
        any_module.log("test")
        out, _ = capfd.readouterr()
        assert out == f"    INFO {created_time} [{Path(__file__).stem}.any_module] test\n"

    def test_LoggersInOtherModulesWillLogWithRootName_PassedRootAndName(self, capfd, created_time):
        root_name = "hoge"
        getLogger(root=True, name=root_name)
        any_module.log("test")
        out, _ = capfd.readouterr()
        assert out == f"    INFO {created_time} [{root_name}.any_module] test\n"

    def test_OutputStackTrace_ErrorRaised(self, capfd, mocker, created_time):
        getLogger(root=True)
        fmt_stack = mocker.spy(Formatter, "formatStack")
        with pytest.raises(ZeroDivisionError):
            raise_zero_div.raise_zero_div()
        out, err = capfd.readouterr()
        fmt_stack.assert_called()
        expected = (
            f"   ERROR {created_time} "
            f"[{Path(__file__).stem}.raise_zero_div] zero div (12:raise_zero_div) \n"
            "Stack (most recent call last):\n"
        )
        assert out.startswith(expected)
        assert err.startswith(expected)
