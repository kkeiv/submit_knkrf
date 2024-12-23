from pymongo.collection import Collection
from pymongo.database import Database
from pymongo import MongoClient, errors
from libs.storage.assets import DBase, Errores


def _connectDatabase(host: str, port: int, dbName: str) -> Database:
    client: MongoClient = MongoClient(host, port)
    return client[dbName]


def loadObjectFull(dbConf: dict, collection: str, idName: str, idValue: str) -> dict:
    # print(f"load: {idValue}")
    if dbConf.get(DBase.db.name, DBase.db.value) == DBase.db.value:
        dbConf[DBase.db.name] = _connectDatabase(host=dbConf.get(DBase.host.name, DBase.host.value),
                                                 port=dbConf.get(DBase.port.name, DBase.port.value),
                                                 dbName=dbConf.get(DBase.name.name, DBase.name.value))

    try:
        _cl: Collection = dbConf[DBase.db.name][collection]
        result = _cl.find_one({idName: idValue})
        return result if result else {}
    except errors.PyMongoError:
        return {}


def saveObject(dbConf: dict, collection: str, idName: str, idValue: str, update: dict) -> str:
    # print(f"save: {idValue}")
    if dbConf.get(DBase.db.name, DBase.db.value) is None:
        dbConf[DBase.db.name] = _connectDatabase(
            host=dbConf.get(DBase.host.name, DBase.host.value),
            port=dbConf.get(DBase.port.name, DBase.port.value),
            dbName=dbConf.get(DBase.name.name, DBase.name.value))

    try:
        _cl: Collection = dbConf[DBase.db.name][collection]
        if idName and idValue:
            _cl.update_one({idName: idValue}, {"$set": update}, upsert=True)
        else:
            _cl.insert_one(update)
        return Errores.noErrore.value
    except errors.PyMongoError:
        return Errores.operationFail.value


def deleteObject(dbConf: dict, collection: str, idName: str, idValue: str) -> str:
    # print(f"delete: {idValue}")
    if dbConf.get(DBase.db.name, DBase.db.value) is None:
        dbConf[DBase.db.name] = _connectDatabase(
            host=dbConf.get(DBase.host.name, DBase.host.value),
            port=dbConf.get(DBase.port.name, DBase.port.value),
            dbName=dbConf.get(DBase.name.name, DBase.name.value))

    try:
        _cl: Collection = dbConf[DBase.db.name][collection]
        _cl.delete_one({idName: idValue})
        return Errores.noErrore.value
    except errors.PyMongoError:
        return Errores.operationFail.value


def loadListItems(dbConf: dict, collection: str, filterName: str = "", filterValue: str = "") -> list:
    # print(f"load: {filterName}={filterValue}")
    if dbConf.get(DBase.db.name, DBase.db.value) is None:
        dbConf[DBase.db.name] = _connectDatabase(
            host=dbConf.get(DBase.host.name, DBase.host.value),
            port=dbConf.get(DBase.port.name, DBase.port.value),
            dbName=dbConf.get(DBase.name.name, DBase.name.value))

    _filter = {}
    if filterName != "" and filterValue != "":
        _filter = {filterName: filterValue}

    try:
        _cl: Collection = dbConf[DBase.db.name][collection]
        _result = list(_cl.find(_filter))
        return _result if _result else []
    except errors.PyMongoError:
        return []
