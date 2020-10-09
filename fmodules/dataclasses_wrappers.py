from dataclasses import field
from numbers import Number


def Default(value):
    return field(**_MakeFieldArg(value), init=True)


def Initial(value):
    return field(**_MakeFieldArg(value), init=False)


def _MakeFieldArg(value):
    return (
        {"default": value}
        if isinstance(value, Number) or (type_ := type(value)) in (str, bytes, type(None), tuple)
        else {"default_factory": type_}
    )
