from typing import AbstractSet, Any, Mapping, Optional, Union

from pydantic.fields import FieldInfo as PydanticFieldInfo
from pydantic.fields import Undefined
from pydantic.typing import NoArgAnyCallable
from pydantic.utils import Representation

IntStr = Union[int, str]
AbstractSetIntStr = AbstractSet[IntStr]
MappingIntStrAny = Mapping[IntStr, Any]


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
    min_items: Optional[int] = None,
    max_items: Optional[int] = None,
    unique_items: Optional[bool] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    allow_mutation: bool = True,
    regex: Optional[str] = None,
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
        min_items=min_items,
        max_items=max_items,
        unique_items=unique_items,
        min_length=min_length,
        max_length=max_length,
        allow_mutation=allow_mutation,
        regex=regex,
        discriminator=discriminator,
        repr=repr,
        **extra,
    )
    field_info._validate()
    return field_info


class _RelationshipInfo(Representation):
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
    relationship_info = _RelationshipInfo(
        local_field=local_field,
        related_field=related_field,
    )
    return relationship_info
