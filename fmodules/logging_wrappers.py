from logging import Logger, getLogger as gL, Formatter, Handler, StreamHandler, FileHandler, LogRecord
from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
from inspect import currentframe, getframeinfo, getargvalues, isfunction, isclass
from typing import Optional, Literal
from pathlib import Path
import sys
import json

from . import pathlib_extensions  # noqa
from .dict_wrapper import AttrDict


_parent: Optional[Logger] = None
_parent_cache: dict[str, Logger] = {}
_children: dict[str, Logger] = {}


def _AddExtraMsg(record: LogRecord) -> Literal[True]:
    record.ex_msg = ""
    if record.levelno in (DEBUG, ERROR, CRITICAL):
        record.ex_msg = f" ({record.lineno}:{record.funcName})"
    return True


def _MakeHandler(handler: type[Handler], level=NOTSET, **kwargs) -> Handler:
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


def _SetParent(child: Logger, parent: Logger) -> None:
    child.name = ".".join([parent.name, child.name.split(".")[-1]])
    child.setLevel(parent.level)
    for hndl in list(child.handlers):
        child.removeHandler(hndl)
    for hndl in parent.handlers:
        child.addHandler(hndl)


def getLogger(name: str, output_dir: Optional[Path] = None, *, root: bool = False) -> Logger:
    global _parent, _parent_cache, _children
    if not root:
        if child := _children.get(name):
            return child
        child = gL(name)
        _SetParent(child, _parent) if _parent else _Setting(child, output_dir)
        _children[name] = child
        return child
    if _parent and _parent.name not in _parent_cache:
        _parent_cache[_parent.name] = _parent
    if not (parent := _parent_cache.get(name)):
        parent = gL(name)
        _Setting(parent, output_dir)
    _parent = parent
    propagate()
    return parent


def propagate() -> None:
    if _parent:
        for child in _children.values():
            _SetParent(child, _parent)


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
