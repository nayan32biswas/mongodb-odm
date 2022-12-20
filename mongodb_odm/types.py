from bson import ObjectId
from bson.dbref import DBRef


class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        elif isinstance(v, str):
            try:
                ObjectId(v)
            except Exception:
                raise TypeError("Invalid ObjectId")
            return v
        raise TypeError("ObjectId required")


class PydanticObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        elif isinstance(v, str):
            return ObjectId(v)
        raise TypeError("Invalid ObjectId required")


class PydanticDBRef(DBRef):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, DBRef):
            return v
        from .models import Document

        if not issubclass(v.__class__, Document) or not hasattr(v, "id"):
            raise TypeError("Invalid Document Model")

        return DBRef(collection=v._get_collection_name(), id=v.id)
