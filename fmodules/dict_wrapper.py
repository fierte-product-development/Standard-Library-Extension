from typing import Any


class AttrDict(dict):
    """AttrDict is a dict allow their elements to be accessed both as keys and as attributes"""

    def __init__(self, *args, **kwargs):
        def CastDict(node):
            if type(node) is dict:
                return AttrDict(node)
            if type(node) is list:
                node = [CastDict(elm) for elm in node]
            return node

        super().__init__(*args, **kwargs)
        for key, val in self.items():
            self[key] = CastDict(val)
        self.__dict__ = self

    def __getattr__(self, name) -> Any:
        raise AttributeError(f"This 'AttrDict' has no attribute '{name}'")
