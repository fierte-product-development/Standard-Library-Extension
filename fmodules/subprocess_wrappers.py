import subprocess
import os
import locale
import re


class subprocessWrappers:
    @classmethod
    def common_setting(cls, *args, **kwargs):
        param = {
            'args': args,
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE,
            'encoding': locale.getpreferredencoding()
        }
        if os.name == 'nt':
            if 'shell' not in kwargs or not kwargs['shell']:
                param['encoding'] = 'utf-8'
            else:
                param['encoding'] = {
                    932: 'cp932',
                    65001: 'utf-8'
                }[cls.GetChcp()]
        kwargs.update(param)
        return kwargs

    @staticmethod
    def GetChcp():
        cp = subprocess.run(**{
            'args': ['chcp'],
            'stdout': subprocess.PIPE,
            'shell': True
        })
        raw = str(cp.stdout)
        match = re.search(r'(: )(?P<chcp>\d+)', raw)
        return int(match.group('chcp'))

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
