from bson.dbref import DBRef


class DurationField(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("Invalid Time Duration")
        temp = v.split(":")
        if len(temp) != 3:
            raise TypeError("Invalid Time Duration")
        if not temp[0].isdigit() or not temp[1].isdigit():
            raise TypeError("Invalid hours or minutes")
        hours, minutes, seconds = int(temp[0]), int(temp[1]), float(temp[2])
        if seconds > 60:
            minutes += int(seconds // 60)
            seconds = seconds % 60
        if minutes > 60:
            hours += int(minutes // 60)
            minutes = minutes % 60
        return f"{hours:02}:{minutes:02}:{seconds:09.6f}"

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(format="00:00:00")


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
