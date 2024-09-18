from typing import Dict, Any
from libs.storage import dbMongo
from libs.storage.assets import dbTypes, _defaultType_, DBase, Table, Errores


def getTypeByName(dbType: str) -> dbTypes:
    if dbType == dbTypes.mongo.value:
        return dbTypes.mongo

    return dbTypes.unknown


class Storage:
    def __init__(self) -> None:
        self._dbs: dict = {}
        self._tables: dict = {}

    def printForLog(self) -> str:
        _dbs = ""
        for _name, _val in self._dbs.items():
            _adds = [f"{_k}:{_v}" for _k, _v in _val.items()]
            _dbs = f"{_dbs}{_name}: {{{'; '.join(_adds)}}}"

        _tbs = ""
        for _name, _val in self._tables.items():
            _adds = [f"{_k}:{_v}" for _k, _v in _val.items()]
            _tbs = f"{_tbs}{_name}: {{{'; '.join(_adds)}}}"
        return f"dbs: {{{_dbs}}}, tables: {{{_tbs}}}"

    def addDatabase(self, config: dict) -> str:
        _db: Dict[str, Any] = {}
        _db[DBase.instance.name] = len(self._dbs)
        _db[DBase.type.name] = getTypeByName(config.get(DBase.type.name, _defaultType_.value))
        _db[DBase.host.name] = config.get(DBase.host.name, DBase.host.value)
        _db[DBase.port.name] = config.get(DBase.port.name, DBase.port.value)
        _db[DBase.name.name] = config.get(DBase.name.name, DBase.name.value)
        _db[DBase.login.name] = config.get(DBase.login.name, DBase.login.value)
        _db[DBase.password.name] = config.get(DBase.password.name, DBase.password.value)
        _db[DBase.default.name] = config.get(DBase.default.name, DBase.default.value)
        _db[DBase.db.name] = None
        self._dbs[_db[DBase.instance.name]] = _db
        return ""

    def deleteDatabase(self) -> str:
        return ""

    def getDefaultDB(self) -> dict:
        for _db in self._dbs.values():
            if _db.get(DBase.default.name, DBase.default.value) != DBase.default.value:
                return _db
        return {}

    def getDatabaseForTable(self, table: str) -> dict:
        if table in self._tables:
            return self._tables[table].get(Table.database.name, self.getDefaultDB())
        else:
            return self.getDefaultDB()

    def loadItemFull(self, table: str, idName: str, idValue: str) -> dict:
        print("loadItem", table, idName, idValue)
        _db: dict = self.getDatabaseForTable(table)

        if _db.get(DBase.type.name, DBase.type) == dbTypes.mongo:
            return dbMongo.loadObjectFull(dbConf=_db,
                                          collection=table,
                                          idName=idName,
                                          idValue=idValue)

        return {}

    def saveItemFull(self, table: str, idName: str, idValue: str, item: dict) -> str:
        # print("save User", table, idName, idValue, item)
        _db: dict = self.getDatabaseForTable(table)

        if _db.get(DBase.type.name, DBase.type) == dbTypes.mongo:
            return dbMongo.saveObject(dbConf=_db,
                                      collection=table,
                                      idName=idName,
                                      idValue=idValue,
                                      update=item)

        return Errores.typeNotSupported.value

    def deleteItem(self, table: str, idName: str, idValue: str) -> str:
        _db: dict = self.getDatabaseForTable(table)

        if _db.get(DBase.type.name, DBase.type) == dbTypes.mongo:
            return dbMongo.deleteObject(dbConf=_db,
                                        collection=table,
                                        idName=idName,
                                        idValue=idValue)

        return Errores.typeNotSupported.value

    def loadListItems(self, table: str, filterName: str = "", filterValue: str = "") -> list:
        _db: dict = self.getDatabaseForTable(table)

        if _db.get(DBase.type.name, DBase.type) == dbTypes.mongo:
            return dbMongo.loadListItems(dbConf=_db,
                                         collection=table,
                                         filterName=filterName,
                                         filterValue=filterValue)

        return []
