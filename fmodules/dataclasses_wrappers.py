from dataclasses import field


def NoneInit():
    return field(default=None, init=False)
