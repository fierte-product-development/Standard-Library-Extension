from logging import Logger, getLogger, Formatter, StreamHandler, FileHandler, DEBUG, INFO
import pathlib
import sys

import pathlib_extensions  # noqa


class loggingWrappers:
    @staticmethod
    def _NewHandler(handler_class, min_lv, **kwargs):
        handler = handler_class(**kwargs)
        handler.setLevel(min_lv)
        handler.setFormatter(Formatter('%(levelname)8s %(asctime)s [%(name)s] %(message)s'))
        return handler

    @classmethod
    def getLogger(cls, output: pathlib.Path, debug=False) -> Logger:
        logger_name = output.name
        min_lv = DEBUG if debug else INFO
        logger = getLogger(logger_name)
        logger.setLevel(min_lv)
        logger.addHandler(cls._NewHandler(StreamHandler, min_lv, **{
            'stream': sys.stdout
        }))
        if not debug:
            output = (output/'log').mkdir_hidden()
            logger.addHandler(cls._NewHandler(FileHandler, min_lv, **{
                'filename': output / f'{logger_name}.log',
                'encoding': 'utf-8',
            }))
        return logger, output


def main():
    log_output = pathlib.Path(__file__).parent
    logger, _ = loggingWrappers.getLogger(log_output)
    logger.debug(f'test_debug')
    logger.info(f'test_info')


if __name__ == "__main__":
    main()
