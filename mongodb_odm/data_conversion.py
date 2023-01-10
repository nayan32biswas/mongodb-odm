from typing import Any


class OdmObj(object):
    def __repr__(self) -> str:
        items = ("{}={!r}".format(k, self.__dict__[k]) for k in self.__dict__)
        return "{}({})".format(type(self).__name__, ", ".join(items))

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__

    def __iter__(self):
        yield from self.__dict__.items()

    def dict(self):
        return _to_dict(self)


def _to_dict(obj):
    if isinstance(obj, list):
        obj = [_to_dict(x) for x in obj]
    if not isinstance(obj, OdmObj):
        return obj

    n_d = {}
    for k, v in obj:
        n_d[k] = _to_dict(v)
    return n_d


def _to_obj(d):
    if isinstance(d, list):
        d = [_to_obj(x) for x in d]
    if not isinstance(d, dict):
        return d

    obj = OdmObj()
    for k, v in d.items():
        obj.__dict__[k] = _to_obj(v)
    return obj


def dict2obj(d: dict) -> Any:
    return _to_obj(d)
