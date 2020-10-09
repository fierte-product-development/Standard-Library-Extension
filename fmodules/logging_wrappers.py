from logging import Logger, getLogger, Formatter, Handler, StreamHandler, FileHandler
from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
from inspect import currentframe, getframeinfo, getargvalues, isfunction, isclass
from typing import Tuple, Optional
from pathlib import Path
import sys
import json

from . import pathlib_extensions  # noqa
from .dict_wrapper import AttrDict


class loggingWrappers:
    _formatter = Formatter("%(levelname)8s %(asctime)s [%(name)s] %(message)s%(ex_func)s")

    @staticmethod
    def _AddExtraArg(record) -> bool:
        record.ex_func = f" ({record.lineno}:{record.funcName})" if record.levelno in (DEBUG, ERROR, CRITICAL) else ""
        return True

    @classmethod
    def _FilterInfoOrUnder(cls, record) -> bool:
        return record.levelno <= INFO

    @classmethod
    def _MakeHandler(cls, handler_class, level=NOTSET, filter_=None, **kwargs) -> Handler:
        handler = handler_class(**kwargs)
        handler.setFormatter(cls._formatter)
        handler.addFilter(cls._AddExtraArg)
        if level:
            handler.setLevel(level)
        if filter_:
            handler.addFilter(filter_)
        return handler

    @classmethod
    def getLogger(cls, name, output_dir: Optional[Path] = None) -> Tuple[Logger, Optional[Path]]:
        logger = getLogger(name)
        logger.setLevel(INFO if output_dir else DEBUG)
        logger.addHandler(cls._MakeHandler(StreamHandler, level=DEBUG, filter_=cls._FilterInfoOrUnder, stream=sys.stdout))
        logger.addHandler(cls._MakeHandler(StreamHandler, level=WARNING, stream=sys.stderr))
        if output_dir:
            log_dir = (output_dir / "log").mkdir_hidden()
            log_file = log_dir / f"{output_dir.resolve().name}.log"
            logger.addHandler(cls._MakeHandler(FileHandler, filename=log_file, encoding="utf-8"))
        else:
            log_file = None
        return logger, log_file


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
