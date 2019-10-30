import pathlib

from subprocess_wrappers import subprocessWrappers


def mkdir_hidden(self) -> pathlib.Path:
    """
    Returns:
        pathlib.Path: A path with a leading '.'.
    """
    renamed = self.parent / f'.{self.name}'
    renamed.mkdir(parents=True, exist_ok=True)
    if type(self) == pathlib.WindowsPath:
        subprocessWrappers.run('attrib', '+H', str(renamed), shell=True)
    return renamed


pathlib.Path.mkdir_hidden = mkdir_hidden
