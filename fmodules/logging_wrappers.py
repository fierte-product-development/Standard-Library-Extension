from logging import Logger, getLogger, Filter, Formatter, Handler, StreamHandler, FileHandler, NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
from typing import Tuple, Optional
import pathlib
import sys
import json

from attrdict import AttrDict
import fmodules.pathlib_extensions  # noqa

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

    @staticmethod
    def GetLogMessages(name, saved_dir: pathlib.Path) -> dict:
        with open(saved_dir/'messages.json', encoding='utf-8') as json_:
            msg = AttrDict(json.loads(json_.read()))
        return msg.name

    @classmethod
    def GetLoggingKit(cls, logger_name, root_dir: pathlib.Path, debug=False) -> Tuple[Logger, dict]:
        """
        Return logger and log message dictionary.
        Log message dictionary must be saved as 'messages.json'.
        """
        logger, _ = cls.getLogger(logger_name, root_dir if not debug else None)
        log_messages = cls.GetLogMessages(logger_name, root_dir)
        return logger, log_messages
