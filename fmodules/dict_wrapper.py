from typing import Any


class AttrDict(dict):
    """This is a dict allow their elements to be accessed both as keys and as attributes."""

    def __init__(self, *args, **kwargs):
        def SearchDictAndReplace(node):
            if type(node) is dict:
                return AttrDict(node)
            if type(node) is list:
                for i, elm in enumerate(node):
                    node[i] = SearchDictAndReplace(elm)
            return node

        super().__init__(*args, **kwargs)
        for key, val in self.items():
            self[key] = SearchDictAndReplace(val)
        self.__dict__ = self

    def __getattr__(self, name) -> Any:
        raise AttributeError
