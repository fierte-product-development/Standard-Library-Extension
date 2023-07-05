from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL, LogRecord, Formatter
import pytest
from pathlib import Path
from time import strftime, localtime
from ..logging_wrappers import getLogger, fFormatter, LevelFilter
from .. import logging_wrappers

from . import any_module, raise_zero_div


@pytest.fixture
def fixed_time(mocker) -> str:
    # `logging.time.time()` will be assigned to `LogRecord.created` attribute.
    # Therefore, log messages' asctime will be fixed.
    ctime = 1000000000
    mocker.patch("logging.time.time", return_value=ctime)
    return strftime("%Y-%m-%d %X", localtime(ctime))


class Test_LevelFilter:
    @pytest.fixture
    def lv_flt(self) -> LevelFilter:
        return LevelFilter(max_level=INFO)

    class Test_filter:
        @pytest.mark.parametrize("lv_no", [DEBUG, INFO])
        def test_OutputMsg_TakesSpecificLevel(self, lv_flt: LevelFilter, lv_no):
            rec = LogRecord("name", lv_no, "pathname", 100, "msg", None, None, func="func")
            assert lv_flt.filter(rec)

        @pytest.mark.parametrize("lv_no", [WARNING, ERROR, CRITICAL])
        def test_DoesNothing_TakesSpecificLevel(self, lv_flt: LevelFilter, lv_no):
            rec = LogRecord("name", lv_no, "pathname", 100, "msg", None, None, func="func")
            assert lv_flt.filter(rec) is False


class Test_fFormatter:
    class Test_format:
        @pytest.fixture
        def fmt(self) -> fFormatter:
            return fFormatter()

        @pytest.mark.parametrize("lv_no, lv_name", [(INFO, "INFO"), (WARNING, "WARNING")])
        def test_OutputMsg_TakesSpecificLevel(self, fmt: fFormatter, fixed_time, lv_no, lv_name):
            rec = LogRecord("name", lv_no, "pathname", 100, "msg", None, None, func="func")
            assert fmt.format(rec) == f"{lv_name:>8} {fixed_time} [pathname] msg"

        @pytest.mark.parametrize("lv_no, lv_name", [(DEBUG, "DEBUG"), (ERROR, "ERROR"), (CRITICAL, "CRITICAL")])
        def test_OutputLineNoAndFuncName_TakesSpecificLevel(self, fmt: fFormatter, fixed_time, lv_no, lv_name):
            rec = LogRecord("name", lv_no, "pathname", 100, "msg", None, None, func="func")
            assert fmt.format(rec) == f"{lv_name:>8} {fixed_time} [pathname] msg (100:func)"

        def test_OutputStackTrace_StackInfoIsStr(self, fmt: fFormatter, fixed_time):
            rec = LogRecord("name", ERROR, "pathname", 100, "msg", None, None, func="func", sinfo="sinfo")
            assert fmt.format(rec) == f"   ERROR {fixed_time} [pathname] msg (100:func) \nsinfo"

        def test_OutputRoot_RootIsNotRecModule(self, fmt: fFormatter, fixed_time, mocker):
            mocker.patch.object(logging_wrappers, "_root", new="_root")
            rec = LogRecord("name", INFO, "pathname", 100, "msg", None, None, func="func")
            assert fmt.format(rec) == f"    INFO {fixed_time} [_root.pathname] msg"


class Test_getLogger:
    def test_DoesNotOutputLogToStream_CalledDebugLogMethod(self, capfd):
        getLogger(root=True)
        any_module.debug("test")
        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

    def test_OutputLogToFile_CalledDebugLogMethod(self, fixed_time, tmp_path: Path):
        getLogger(tmp_path, root=True)
        any_module.debug("test")
        log_file = tmp_path / ".log" / f"{tmp_path.resolve().name}.log"
        assert log_file.read_text() == f"   DEBUG {fixed_time} [{Path(__file__).stem}.any_module] test (12:debug)\n"

    def test_OutputInfoLog_TakesSpecificLevel(self, capfd, fixed_time):
        getLogger(root=True)
        any_module.info("test")
        out, err = capfd.readouterr()
        assert out == f"    INFO {fixed_time} [{Path(__file__).stem}.any_module] test\n"
        assert err == ""

    def test_OutputWarningLog_TakesSpecificLevel(self, capfd, fixed_time):
        getLogger(root=True)
        any_module.warning("test")
        out, err = capfd.readouterr()
        assert out == ""
        assert err == f" WARNING {fixed_time} [{Path(__file__).stem}.any_module] test\n"

    def test_OutputErrorLog_TakesSpecificLevel(self, capfd, fixed_time):
        getLogger(root=True)
        any_module.error("test")
        out, err = capfd.readouterr()
        assert out == ""
        assert err == f"   ERROR {fixed_time} [{Path(__file__).stem}.any_module] test (24:error)\n"

    def test_OutputCriticalLog_TakesSpecificLevel(self, capfd, fixed_time):
        getLogger(root=True)
        any_module.critical("test")
        out, err = capfd.readouterr()
        assert out == ""
        assert err == f"CRITICAL {fixed_time} [{Path(__file__).stem}.any_module] test (28:critical)\n"

    def test_LoggersInOtherModulesWillLogWithMyName_PassedTrueToRoot(self, capfd, fixed_time):
        getLogger(root=True)
        any_module.info("test")
        out, _ = capfd.readouterr()
        assert out == f"    INFO {fixed_time} [{Path(__file__).stem}.any_module] test\n"

    def test_LoggersInOtherModulesWillLogWithRootName_PassedRootAndName(self, capfd, fixed_time):
        root_name = "hoge"
        getLogger(root=True, name=root_name)
        any_module.info("test")
        out, _ = capfd.readouterr()
        assert out == f"    INFO {fixed_time} [{root_name}.any_module] test\n"

    def test_OutputStackTrace_ErrorRaised(self, capfd, mocker, fixed_time):
        getLogger(root=True)
        fmt_stack = mocker.spy(Formatter, "formatStack")
        with pytest.raises(ZeroDivisionError):
            raise_zero_div.raise_zero_div()
        out, err = capfd.readouterr()
        fmt_stack.assert_called()
        expected = (
            f"   ERROR {fixed_time} "
            f"[{Path(__file__).stem}.raise_zero_div] zero div (12:raise_zero_div) \n"
            "Stack (most recent call last):\n"
        )
        assert out == ""
        assert err.startswith(expected)
