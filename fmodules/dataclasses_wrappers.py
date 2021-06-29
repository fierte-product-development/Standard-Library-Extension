from typing import TypeVar, Union, Any, overload
from dataclasses import field


T = TypeVar("T")


def Default(value: Union[T, type[T]]) -> T:
    return field(**_MakeFieldArg(value), init=True)


class nil:
    pass


@overload
def Initial() -> Any:
    ...


@overload
def Initial(value: Union[T, type[T]]) -> T:
    ...


def Initial(value=nil):
    return field(**_MakeFieldArg(value), init=False)


def _MakeFieldArg(value) -> dict:
    if value is nil:
        return {}
    if isinstance(value, type):
        return {"default_factory": value}
    return {"default": value}
