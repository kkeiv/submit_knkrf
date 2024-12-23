from typing import Optional, Any
from enum import Enum
from libs.common.classes import Parameter
from pymongo.database import Database


class Errores(Enum):
    noDatabase = "empty_database_list"
    typeNotSupported = "database_with_type_not_supported"

    noCollection = "no collection"
    operationFail = "operation fail"

    noErrore = ""


class dbTypes(Enum):
    unknown = "unknown"
    mongo = "mongodb"


_defaultType_ = dbTypes.mongo


class DBase(Enum):
    default: Parameter = Parameter(name="default", kind=bool, default=True)
    dbtype: Parameter = Parameter(name="dbtype", kind=dbTypes, default=_defaultType_)
    host: Parameter = Parameter(name="host", kind=str, default="localhost")
    port: Parameter = Parameter(name="port", kind=int, default=27017)
    dbname: Parameter = Parameter(name="dbname", kind=str, default="database_name")
    login: Parameter = Parameter(name="login", kind=str, default="db_login")
    password: Parameter = Parameter(name="password", kind=str, default="db_password")
    mirrors: Parameter = Parameter(name="mirrors", kind=list, default=[])
    instance: Parameter = Parameter(name="instance", kind=int, default=-1)
    additional: Parameter = Parameter(name="additional", kind=str, default="")
    db: Parameter = Parameter(name="db", kind=Database, default=None)


class Table(Enum):
    database: Optional[DBase] = None
    cl = None
