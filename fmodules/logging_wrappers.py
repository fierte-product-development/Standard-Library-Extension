from logging import Logger, getLogger as gL, Formatter, Handler, StreamHandler, FileHandler, LogRecord
from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
from inspect import currentframe, getframeinfo, getargvalues, isfunction, isclass
from typing import TypeVar, Optional, Literal
from pathlib import Path
import sys
import json

from . import pathlib_extensions  # noqa
from .dict_wrapper import AttrDict


HandlerT = TypeVar("HandlerT", bound=Handler)
_loggers: dict[str, Logger] = {}


def _AddExtraMsg(record: LogRecord) -> Literal[True]:
    record.ex_msg = ""
    if record.levelno in (DEBUG, ERROR, CRITICAL):
        record.ex_msg = f" ({record.lineno}:{record.funcName})"
    return True


def _MakeHandler(handler: type[HandlerT], level=NOTSET, **kwargs) -> HandlerT:
    hndl = handler(**kwargs)
    hndl.setLevel(level)
    hndl.setFormatter(Formatter("%(levelname)8s %(asctime)s [%(name)s] %(message)s%(ex_msg)s"))
    hndl.addFilter(_AddExtraMsg)
    return hndl


def _Setting(logger: Logger, output_dir: Optional[Path]) -> None:
    logger.setLevel(INFO if output_dir else DEBUG)
    logger.addHandler(_MakeHandler(StreamHandler, level=DEBUG, stream=sys.stdout))
    logger.addHandler(_MakeHandler(StreamHandler, level=WARNING, stream=sys.stderr))
    if output_dir:
        log_dir = (output_dir / "log").mkdir_hidden()
        log_file = log_dir / f"{output_dir.resolve().name}.log"
        logger.addHandler(_MakeHandler(FileHandler, filename=log_file, encoding="utf-8"))


def _Copy(src: Logger, dst: Logger) -> None:
    dst.setLevel(src.level)
    for hndl in dst.handlers:
        dst.removeHandler(hndl)
    for hndl in src.handlers:
        dst.addHandler(hndl)


def getLogger(name: str, output_dir: Optional[Path] = None, *, root: bool = False) -> Logger:
    if existing := _loggers.get(name):
        return existing
    logger = gL(name)
    if not root:
        _loggers[name] = logger
        _Copy(_loggers["root"], logger) if "root" in _loggers else _Setting(logger, output_dir)
        return logger
    _Setting(logger, output_dir)
    for existing in _loggers.values():
        _Copy(logger, existing)
    _loggers[name] = logger
    _loggers["root"] = logger
    return logger


def SetLogMessages() -> None:
    """
    Set `_log_msg` attribute of each object to the message contained in 'messages.json'.
    'messages.json' must be in the same directory as the caller's `.py` file.
    """
    if (caller := currentframe().f_back) is None:
        raise RuntimeError
    caller_path = Path(getframeinfo(caller).filename)
    caller_name, caller_dir = caller_path.stem, caller_path.parent
    msgs = (caller_dir / "messages.json").read_text("utf-8")
    msg = AttrDict(json.loads(msgs)[caller_name])
    for name, obj in caller.f_locals.items():
        if (isfunction(obj) or isclass(obj)) and name in msg:
            if hasattr(obj, "_log_msg"):
                obj._log_msg = AttrDict(obj._log_msg)
                obj._log_msg.update(msg[name])
            else:
                obj._log_msg = msg[name]


def logmsg() -> AttrDict:
    """
    Returns:
        AttrDict: One of the following
            {caller module}.globals()[{caller class}]._log_msg[{caller function}]
            {caller module}.globals()[{caller function}]._log_msg
    """
    if (caller := currentframe().f_back) is None:
        raise RuntimeError
    func_name = getframeinfo(caller).function
    args = getargvalues(caller)
    return (
        args.locals[first_arg]._log_msg[func_name]
        if args.args and (first_arg := args.args[0]) in ["self", "cls"]
        else caller.f_globals[func_name]._log_msg
    )
