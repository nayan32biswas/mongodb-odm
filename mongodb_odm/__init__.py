__version__ = "1.0.0"

from pydantic import BaseModel as BaseModel
from pydantic import ConfigDict as ConfigDict
from pymongo import ASCENDING as ASCENDING
from pymongo import DESCENDING as DESCENDING
from pymongo import TEXT as TEXT
from pymongo.operations import DeleteMany as DeleteMany
from pymongo.operations import DeleteOne as DeleteOne
from pymongo.operations import IndexModel as IndexModel
from pymongo.operations import InsertOne as InsertOne
from pymongo.operations import ReplaceOne as ReplaceOne
from pymongo.operations import UpdateMany as UpdateMany
from pymongo.operations import UpdateOne as UpdateOne

from .connection import connect as connect
from .connection import disconnect as disconnect
from .fields import Field as Field
from .fields import Relationship as Relationship
from .models import Document as Document
from .types import ObjectIdStr as ObjectIdStr
from .types import ODMObjectId as ODMObjectId
from .utils.apply_indexes import apply_indexes as apply_indexes
