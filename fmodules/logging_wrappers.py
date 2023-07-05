from logging import Logger, getLogger as gL, Formatter, Handler, StreamHandler, FileHandler, LogRecord
from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
from time import strftime, localtime
from inspect import getargvalues, isfunction, isclass
from typing import Optional
from pathlib import Path
import sys
import json

from . import pathlib_extensions  # noqa
from .inspect_wrappers import previousframe
from .dict_wrapper import AttrDict


_root: str = ""


class LevelFilter:
    def __init__(self, max_level: int):
        self.max_level = max_level

    def filter(self, record: LogRecord):
        return record.levelno <= self.max_level


class fFormatter(Formatter):
    def format(self, rec: LogRecord) -> str:
        lv = f"{rec.levelname:>8}"
        time = strftime("%Y-%m-%d %X", localtime(rec.created))
        mod = f"[{(_root + '.') if _root and _root != rec.module else ''}{rec.module}]"
        msg = rec.getMessage()
        msgs = [lv, time, mod, msg]
        if rec.levelno in (DEBUG, ERROR, CRITICAL):
            msgs.append(f"({rec.lineno}:{rec.funcName})")
        if rec.stack_info:
            msgs.append(f"\n{self.formatStack(rec.stack_info)}")
        return " ".join(msgs)


_fmt = fFormatter()


def _MakeHandler(handler: type[Handler], min_level: int = NOTSET, max_level: int = CRITICAL, **kwargs) -> Handler:
    hndl = handler(**kwargs)
    hndl.setLevel(min_level)
    hndl.setFormatter(_fmt)
    hndl.addFilter(LevelFilter(max_level))
    return hndl


def getLogger(output_dir: Optional[Path] = None, *, root: bool = False, name: str = "") -> Logger:
    """
    `getLogger` will always return a logger with the same name(__package__)
    These loggers change their behavior depending on the three arguments that passed to `getLogger` *last*

    Args:
        output_dir (Path, optional): Logger will Output a .log file to the specified path. Defaults to None.
        root (bool, optional): The name of module that called `getLogger` last is added to log messages. Defaults to False.
        name (str, optional): You can directly specify the name to be added to log messages. Defaults to "".
    """
    if root:
        global _root
        _root = name if name else Path(previousframe(2).filename).stem
    logger = gL(__package__)
    for hndl in list(logger.handlers):
        logger.removeHandler(hndl)
    logger.setLevel(DEBUG)
    logger.addHandler(_MakeHandler(StreamHandler, min_level=DEBUG, max_level=INFO, stream=sys.stdout))
    logger.addHandler(_MakeHandler(StreamHandler, min_level=WARNING, stream=sys.stderr))
    if output_dir:
        log_dir = (output_dir / "log").mkdir_hidden()
        log_file = log_dir / f"{output_dir.resolve().name}.log"
        logger.addHandler(_MakeHandler(FileHandler, filename=log_file, encoding="utf-8"))
    return logger


def SetLogMessages() -> None:
    """
    Set `_log_msg` attribute of each object to the message contained in 'messages.json'.
    'messages.json' must be in the same directory as the caller's `.py` file.
    """
    caller = previousframe(2)
    caller_path = Path(caller.filename)
    caller_name, caller_dir = caller_path.stem, caller_path.parent
    msgs = (caller_dir / "messages.json").read_text("utf-8")
    msg = AttrDict(json.loads(msgs)[caller_name])
    for name, obj in caller.frame.f_locals.items():
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
    caller = previousframe(2)
    func_name = caller.function
    args = getargvalues(caller.frame)
    return (
        args.locals[first_arg]._log_msg[func_name]
        if args.args and (first_arg := args.args[0]) in ["self", "cls"]
        else caller.frame.f_globals[func_name]._log_msg
    )
