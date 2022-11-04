import re

pattern = re.compile(r"(?<!^)(?=[A-Z])")


def camel_to_snake(string: str) -> str:
    return pattern.sub("_", string).lower()
