from collections.abc import Mapping
from typing import AbstractSet, Any, Callable, Optional, Union

from pydantic._internal._repr import Representation as PydanticRepresentation
from pydantic.fields import FieldInfo as PydanticFieldInfo
from pydantic_core import PydanticUndefined as Undefined

IntStr = Union[int, str]
AbstractSetIntStr = AbstractSet[IntStr]
MappingIntStrAny = Mapping[IntStr, Any]
NoArgAnyCallable = Callable[[], Any]


class FieldInfo(PydanticFieldInfo):
    def __init__(self, default: Any = Undefined, **kwargs: Any) -> None:
        super().__init__(default=default, **kwargs)


def Field(
    default: Any = Undefined,
    *,
    default_factory: Optional[NoArgAnyCallable] = None,
    alias: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    exclude: Union["AbstractSetIntStr", "MappingIntStrAny", Any] = None,
    include: Union["AbstractSetIntStr", "MappingIntStrAny", Any] = None,
    const: Optional[bool] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    multiple_of: Optional[float] = None,
    allow_inf_nan: Optional[bool] = None,
    max_digits: Optional[int] = None,
    decimal_places: Optional[int] = None,
    unique_items: Optional[bool] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    frozen: bool = True,
    pattern: Optional[str] = None,
    discriminator: Optional[str] = None,
    repr: bool = True,
    **extra: Any,
) -> Any:
    # Extend Pydantic Field to have more control on the Field
    field_info = FieldInfo(
        default,
        default_factory=default_factory,
        alias=alias,
        title=title,
        description=description,
        exclude=exclude,
        include=include,
        const=const,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        multiple_of=multiple_of,
        allow_inf_nan=allow_inf_nan,
        max_digits=max_digits,
        decimal_places=decimal_places,
        unique_items=unique_items,
        min_length=min_length,
        max_length=max_length,
        frozen=frozen,
        pattern=pattern,
        discriminator=discriminator,
        repr=repr,
        **extra,
    )
    return field_info


class RelationshipInfo(PydanticRepresentation):
    def __init__(
        self,
        *,
        local_field: str,
        related_field: Optional[str] = None,
    ) -> None:
        self.local_field = local_field
        self.related_field = related_field


def Relationship(
    *,
    local_field: str,
    related_field: Optional[str] = None,
) -> Any:
    """
    This is a field of Representation.
    That represents another model as the field type.
    """
    relationship_info = RelationshipInfo(
        local_field=local_field,
        related_field=related_field,
    )
    return relationship_info
