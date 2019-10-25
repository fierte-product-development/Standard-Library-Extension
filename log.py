from logging import Logger, getLogger, Formatter, StreamHandler, FileHandler, DEBUG, INFO
from dataclasses import dataclass, InitVar
import pathlib
import subprocess


def mkdir_hidden(self):
    path = self.resolve()
    if path.name[0] != '.':
        path = path.parent / f'.{path.name}'
    path.mkdir(exist_ok=True)
    if type(self) == pathlib.WindowsPath:
        cmd = ['attrib', '+H', str(path)]
        subprocess.run(cmd, shell=True)
    return path


pathlib.Path.mkdir_hidden = mkdir_hidden


@dataclass
class Log:
    debug: InitVar[bool] = False

    def __post_init__(self, debug):
        self.level = DEBUG if debug else INFO

    def _NewHandler(self, handler_class, **kwargs):
        handler = handler_class(**kwargs)
        handler.setLevel(self.level)
        handler.setFormatter(Formatter('%(levelname)8s %(asctime)s [%(name)s] %(message)s'))
        return handler

    def getLogger(self, path) -> Logger:
        log_name = path.name
        logger = getLogger(log_name)
        logger.setLevel(self.level)
        logger.addHandler(self._NewHandler(StreamHandler))
        if self.level != DEBUG:
            log_dir = (path/'log').mkdir_hidden()
            logger.addHandler(self._NewHandler(FileHandler, **{
                'filename': log_dir / f'{log_name}.log',
                'encoding': 'utf-8',
            }))
        return logger


def main():
    log_dir = pathlib.Path(__file__).parent
    logger = Log().getLogger(log_dir)
    logger.debug(f'test_debug')
    logger.info(f'test_info')


if __name__ == "__main__":
    main()
