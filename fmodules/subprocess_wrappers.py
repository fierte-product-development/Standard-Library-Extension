import subprocess
import os
import locale


class subprocessWrappers:
    @staticmethod
    def run(*args, **kwargs):
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
        cp = subprocess.run(**kwargs)
        return cp
