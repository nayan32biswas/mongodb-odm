import re
from typing import Any

pattern = re.compile(r"(?<!^)(?=[A-Z])")


def camel_to_snake(string: str) -> str:
    return pattern.sub("_", string).lower()


def convert_model_to_collection(model: Any) -> str:
    if (
        hasattr(model.Config, "collection_name")
        and model.Config.collection_name is not None
    ):
        """By default model has Config in Basemodel"""
        return model.Config.collection_name
    else:
        return camel_to_snake(model.__name__)
