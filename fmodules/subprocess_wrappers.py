from subprocess import run, Popen, PIPE, CompletedProcess
import os
import locale
import re


class subprocessWrappers:
    """
    This is a wrapper of subprocess.run and Popen.
    This wrapper executes run and Popen with appropriate encoding on Windows/Linux and capture settings.
    """

    @classmethod
    def run(cls, *args, **kwargs) -> CompletedProcess:
        param = cls._common_setting(*args, **kwargs)
        cp = run(**param)
        return cp

    @classmethod
    def Popen(cls, *args, **kwargs) -> Popen:
        param = cls._common_setting(*args, **kwargs)
        popen = Popen(**param)
        return popen

    @classmethod
    def _common_setting(cls, *args, **kwargs) -> dict:
        overwritee = {
            "shell": False,
        }
        overwriter = {
            "args": args,
            "stdout": PIPE,
            "stderr": PIPE,
            "encoding": locale.getpreferredencoding(),
        }
        # TODO: Python3.9 overwritee | kwargs | overwriter
        new_args = {**overwritee, **kwargs, **overwriter}
        if os.name == "nt":
            new_args["encoding"] = "utf-8" if not new_args["shell"] else {932: "cp932", 65001: "utf-8"}[cls._GetChcp()]
        return new_args

    @classmethod
    def _GetChcp(cls) -> int:
        cp = run(args=["chcp"], stdout=PIPE, shell=True)
        raw = str(cp.stdout)
        match = re.search(r"(: )(?P<chcp>\d+)", raw)
        return int(match.group("chcp"))
