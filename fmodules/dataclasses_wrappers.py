from typing import Any
from dataclasses import field


def Default(value) -> Any:
    return field(**_MakeFieldArg(value), init=True)


class noninit:
    pass


def Initial(value=noninit) -> Any:
    return field(**_MakeFieldArg(value), init=False)


def _MakeFieldArg(value) -> dict:
    if value is noninit:
        return {}
    if isinstance(value, type):
        return {"default_factory": value}
    return {"default": value}
