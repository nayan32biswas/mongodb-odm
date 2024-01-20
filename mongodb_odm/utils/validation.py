import logging
from typing import Any

from mongodb_odm.types import DICT_TYPE

logger = logging.getLogger()


def validate_filter_dict(model: Any, filter: DICT_TYPE) -> bool:
    """
    Field validation: Raise an error if a user passes a filter dict,
    where the dict has some field that does not exist in the model.

    This function will validate only the top level of the field.
    It won't be looking into deep nested fields.
    """
    fields = model.get_parent_child_fields()
    for key in filter.keys():
        if key[0] == "$":
            # this is should be mongodb reserved keys like $or, $and, $text etc
            continue
        if key in fields or key == "_id":
            # Valid single field
            continue
        if "." in key:
            key_list = key.split(".")
            first_key = key_list[0]
            """
            Here the first_key is the field that is defined in the top level of the model.
            Not embedded/nested. But this field may contain nested data.
            """
            if first_key not in fields:
                raise ValueError(f"Invalid key '{key}'. '{key_list[0]}' not found")

            """
            In this section, we will only check the embedded field.
            """
            temp_obj = fields[first_key].type_
            for nested_key in key_list[1:]:
                if nested_key not in temp_obj.model_fields:
                    raise ValueError(f"Invalid key '{key}'. '{nested_key}' not found")
                temp_obj = temp_obj.model_fields[nested_key].type_
            continue
        raise ValueError(f"Invalid key {key}")

    return True
