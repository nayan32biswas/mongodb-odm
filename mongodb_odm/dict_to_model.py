from typing import Any, List


class Object:
    def from_list(self, values) -> List[Any]:
        temp = []
        for v in values:
            if isinstance(v, dict):
                temp.append(Object(**v))
            elif isinstance(v, list) or isinstance(v, tuple):
                temp.append(self.from_list(v))
            else:
                temp.append(v)
        return temp

    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)
        for k, v in kwargs.items():
            if isinstance(v, dict):
                # setattr(self, k, Object(**v))
                self.__dict__[k] = Object(**v)
            elif isinstance(v, list) or isinstance(v, tuple):
                # setattr(self, k, self.from_list(v))
                self.__dict__[k] = self.from_list(v)
            else:
                # setattr(self, k, v)
                self.__dict__[k] = v

    def __repr__(self) -> str:
        items = ("{}={!r}".format(k, self.__dict__[k]) for k in self.__dict__)
        return "{}({})".format(type(self).__name__, ", ".join(items))

    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__
