import subprocess
import os
import locale


class subprocessWrappers:
    @staticmethod
    def common_setting(*args, **kwargs):
        param = {
            'args': args,
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE,
            'encoding': locale.getpreferredencoding()
        }
        # WindowsでShellがFalse(デフォルト)の場合はutf-8
        if os.name == 'nt' and 'shell' not in kwargs:
            param['encoding'] = 'utf-8'
        kwargs.update(param)
        return kwargs

    @classmethod
    def run(cls, *args, **kwargs):
        param = cls.common_setting(*args, **kwargs)
        cp = subprocess.run(**param)
        return cp

    @classmethod
    def Popen(cls, *args, **kwargs):
        param = cls.common_setting(*args, **kwargs)
        popen = subprocess.Popen(**param)
        return popen
