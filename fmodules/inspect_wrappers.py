from inspect import currentframe, getframeinfo, FrameInfo


def previousframe(back: int = 1, context=1) -> FrameInfo:
    if (cf := currentframe()) is None:
        raise RuntimeError
    for _ in range(back):
        if (cf := cf.f_back) is None:
            raise RuntimeError
    return FrameInfo(cf, *getframeinfo(cf, context))
