import logging
from typing import Any

from mongodb_odm.types import DICT_TYPE

logger = logging.getLogger()


def validate_filter_dict(model: Any, filter: DICT_TYPE) -> bool:
    fields = model.__fields__
    for key in filter.keys():
        if key[0] == "$":
            # this is should be mongodb reserved keys like $or, $and, $text etc
            continue
        if key in fields or key == "_id":
            # Valid single field
            continue
        if "." in key:
            temp_obj = model
            for nested_key in key.split("."):
                if nested_key not in temp_obj.__fields__:
                    raise ValueError(f"Invalid key '{key}'. '{nested_key}' not found")
                temp_obj = temp_obj.__fields__[nested_key].type_
            continue
        raise ValueError(f"Invalid key {key}")

    return True
