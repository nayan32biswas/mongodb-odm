from typing import Any


class OdmObj(object):
    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__

    def dict(self) -> dict:
        return self.__dict__

    def __repr__(self) -> str:
        items = ("{}={!r}".format(k, self.__dict__[k]) for k in self.__dict__)
        return "{}({})".format(type(self).__name__, ", ".join(items))

    def __str__(self) -> str:
        return self.__repr__()


def __to_obj(d):
    if isinstance(d, (list, tuple)):
        d = [__to_obj(x) for x in d]
    if not isinstance(d, dict):
        return d

    obj = OdmObj()
    for k in d:
        obj.__dict__[k] = __to_obj(d[k])
    return obj


def dict2obj(d: dict) -> Any:
    return __to_obj(d)
