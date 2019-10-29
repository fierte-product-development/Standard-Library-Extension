from logging import Logger, getLogger, Filter, Formatter, StreamHandler, FileHandler, NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
import pathlib
import sys

import pathlib_extensions  # noqa


class loggingWrappers:
    _formatter = Formatter('%(levelname)8s %(asctime)s [%(name)s] %(message)s%(func_)s')

    @staticmethod
    def _AddLineNo(record):
        record.func_ = f' ({record.lineno}:{record.funcName})' \
            if record.levelno in (DEBUG, ERROR, CRITICAL) else ''
        return True

    @staticmethod
    def _FilterInfoOrUnder(record):
        return record.levelno <= INFO

    @classmethod
    def _NewHandler(cls, handler_class, level=NOTSET, filter_=None, **kwargs):
        handler = handler_class(**kwargs)
        handler.setFormatter(cls._formatter)
        handler.addFilter(cls._AddLineNo)
        if level:
            handler.setLevel(level)
        if filter_:
            handler.addFilter(filter_)
        return handler

    @classmethod
    def getLogger(cls, output_to: pathlib.Path, debug=False):
        logger_name = output_to.name
        logger = getLogger(logger_name)
        logger.setLevel(INFO if not debug else DEBUG)
        logger.addHandler(cls._NewHandler(StreamHandler, **{
            'level': DEBUG,
            'filter_': cls._FilterInfoOrUnder,
            'stream': sys.stdout,
        }))
        logger.addHandler(cls._NewHandler(StreamHandler, **{
            'level': WARNING,
            'stream': sys.stderr,
        }))
        if not debug:
            save_dir = (output_to/'log').mkdir_hidden()
            log_file = save_dir / f'{logger_name}.log'
            logger.addHandler(cls._NewHandler(FileHandler, **{
                'filename': log_file,
                'encoding': 'utf-8',
            }))
        return logger, log_file if not debug else None


def main():
    log_dir = pathlib.Path(__file__).parent
    logger, _ = loggingWrappers.getLogger(log_dir)
    logger.debug(f'test_debug')
    logger.info(f'test_info')
    logger.warning(f'test_warning')
    logger.error(f'test_error')
    logger.critical(f'test_critical')


if __name__ == "__main__":
    main()
