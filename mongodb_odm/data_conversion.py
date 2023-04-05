from typing import Any, Dict, Generator, List, Union


class ODMObj(object):
    def __repr__(self) -> str:
        items = ("{}={!r}".format(k, self.__dict__[k]) for k in self.__dict__)
        return "{}({})".format(type(self).__name__, ", ".join(items))

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, other: object) -> bool:
        return self.__dict__ == other.__dict__

    def __iter__(self) -> Generator[tuple[str, Any], None, None]:
        yield from self.__dict__.items()

    def dict(self) -> Any:
        return _to_dict(self)


def _to_dict(obj: Any) -> Any:
    if isinstance(obj, list):
        obj = [_to_dict(x) for x in obj]
    if not isinstance(obj, ODMObj):
        return obj

    n_d = {}
    for k, v in obj:
        n_d[k] = _to_dict(v)
    return n_d


def _to_obj(d: Union[Dict[str, Any], List[Any]]) -> Any:
    if isinstance(d, list):
        d = [_to_obj(x) for x in d]
    if not isinstance(d, dict):
        return d

    obj = ODMObj()
    for k, v in d.items():
        obj.__dict__[k] = _to_obj(v)
        if k == "_id":
            obj.__dict__["id"] = obj.__dict__[k]
    return obj


def dict2obj(d: Dict[str, Any]) -> Any:
    return _to_obj(d)
