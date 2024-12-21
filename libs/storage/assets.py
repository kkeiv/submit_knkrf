from typing import Optional, Any
from enum import Enum


class Errores(Enum):
    noDatabase = "empty_database_list"
    typeNotSupported = "database_with_type_not_supported"

    noCollection = "no collection"
    operationFail = "operation fail"

    noErrore = ""


class dbTypes(Enum):
    unknown = "unknown"
    mongo = "mongo"


_defaultType_ = dbTypes.mongo


class DBase(Enum):
    default: bool = False
    type: dbTypes = _defaultType_
    host: str = "localhost"
    port: int = 27017
    name: str = "my_database"
    login: str = ""
    password: str = ""
    instance: int = -1
    db: Optional[Any] = None


class Table(Enum):
    database: Optional[DBase] = None
    cl = None
