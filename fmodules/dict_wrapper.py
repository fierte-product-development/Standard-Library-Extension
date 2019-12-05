class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, val in self.items():
            if type(val) is dict:
                self[key] = AttrDict(val)
        self.__dict__ = self
