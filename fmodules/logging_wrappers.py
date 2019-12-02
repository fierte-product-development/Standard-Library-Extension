from logging import Logger, getLogger, Filter, Formatter, Handler, StreamHandler, FileHandler, NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
import inspect
from typing import Tuple, Optional
import pathlib
import sys
import json

import fmodules.pathlib_extensions  # noqa
from attrdict import AttrDict


class loggingWrappers:
    _formatter = Formatter('%(levelname)8s %(asctime)s [%(name)s] %(message)s%(ex_func)s')

    @staticmethod
    def _AddExtraArg(record) -> bool:
        record.ex_func = f' ({record.lineno}:{record.funcName})' \
            if record.levelno in (DEBUG, ERROR, CRITICAL) else ''
        return True

    @staticmethod
    def _FilterInfoOrUnder(record) -> bool:
        return record.levelno <= INFO

    @classmethod
    def _NewHandler(cls, handler_class, level=NOTSET, filter_=None, **kwargs) -> Handler:
        handler = handler_class(**kwargs)
        handler.setFormatter(cls._formatter)
        handler.addFilter(cls._AddExtraArg)
        if level:
            handler.setLevel(level)
        if filter_:
            handler.addFilter(filter_)
        return handler

    @classmethod
    def getLogger(cls, name, output_dir: Optional[pathlib.Path] = None) -> Tuple[Logger, Optional[pathlib.Path]]:
        logger = getLogger(name)
        logger.setLevel(INFO if output_dir else DEBUG)
        logger.addHandler(cls._NewHandler(StreamHandler, **{
            'level': DEBUG,
            'filter_': cls._FilterInfoOrUnder,
            'stream': sys.stdout,
        }))
        logger.addHandler(cls._NewHandler(StreamHandler, **{
            'level': WARNING,
            'stream': sys.stderr,
        }))
        if output_dir:
            log_dir = (output_dir/'log').mkdir_hidden()
            log_file = log_dir / f'{output_dir.resolve().name}.log'
            logger.addHandler(cls._NewHandler(FileHandler, **{
                'filename': log_file,
                'encoding': 'utf-8',
            }))
        return logger, log_file if output_dir else None


class loggingTools:
    @staticmethod
    def GetLogMessages(file_: pathlib.Path) -> dict:
        """
        Return logger and log message dictionary.
        Log message dictionary must be saved as 'messages.json'.

        Args:
            file_ (pathlib.Path): `pathlib.Path(__file__)`
        """
        name, saved_dir = file_.stem, file_.parent
        with open(saved_dir/'messages.json', encoding='utf-8') as json_:
            msg = json.loads(json_.read())
        return msg[name]

    @staticmethod
    def SetMethodLogMessages(cls_):
        cls_messages = cls_.logmsg
        for name, method in inspect.getmembers(cls_, inspect.isfunction):
            if name in cls_messages:
                method.logmsg = AttrDict(cls_messages[name])

    @staticmethod
    def GetMethodLogMessages(cls_):
        method_name = inspect.stack()[1].function
        for name, func in inspect.getmembers(cls_, inspect.isfunction):
            if name == method_name:
                return func.logmsg
