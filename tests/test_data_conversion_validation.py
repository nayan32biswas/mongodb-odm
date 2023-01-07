import logging

from bson import ObjectId

from .conftest import init_config  # noqa
from mongodb_odm.data_conversion import dict2obj

logger = logging.getLogger(__name__)


monogdb_data = {
    "list": [1, 2],
    "bytes": bytes(b"ABC"),
    "dict_data": {"a": 1, "b": 2},
    "code": {},
    "ObjectId": ObjectId(),
    "nested_dict": {
        "a": {"a": "ABC"},
        "b": {"a": 1},
    },
    "deep_obj": {
        "a": {"a": [1, 2, 3]},
        "b": [{"a"}],
    },
}


def test_dict2obj():
    obj = dict2obj(monogdb_data)

    assert isinstance(obj.list, list)
    assert isinstance(obj.bytes, bytes)

    assert obj.list[0] == monogdb_data["list"][0]
    assert obj.nested_dict.a.a == monogdb_data["nested_dict"]["a"]["a"]


def test_obj_equality():
    data = {
        "a": {"a": [1, 2]},
        "b": {"a": {"a": 5}},
    }
    obj = dict2obj(data)
    obj1 = dict2obj(data)

    assert obj == obj1
    obj1.c = 1
    assert obj != obj1


def test_obj2dict():
    obj = dict2obj(monogdb_data)

    assert monogdb_data == obj.dict()


def test_odm_obj_str():
    obj = dict2obj(monogdb_data)

    assert isinstance(str(obj), str)
