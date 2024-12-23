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

    def printForLog(self, debug: bool = False) -> str:
        _dbs = ""
        for _name, _val in self._dbs.items():
            if debug:
                _adds = [f"{_k}:{_v}" for _k, _v in _val.items()]
            else:
                _adds = [f"{_k}:{_v}" for _k, _v in _val.items() if "password" not in _k]
            _dbs = f"{_dbs}{_name}: {{{'; '.join(_adds)}}}"

        _tbs = ""
        for _name, _val in self._tables.items():
            _tbs = f"{_tbs}{_name}: {_val}"
        return f"dbs: {{{_dbs}}}, tables: {{{_tbs}}}"

    def addDatabase(self, config: dict) -> str:
        _db: Dict[str, Any] = {}
        _db[DBase.instance.name] = len(self._dbs)
        _db[DBase.dbtype.name] = getTypeByName(config.get(DBase.dbtype.name, _defaultType_.value))
        _db[DBase.host.name] = config.get(DBase.host.name, DBase.host.default)
        _db[DBase.port.name] = config.get(DBase.port.name, DBase.port.default)
        _db[DBase.dbname.name] = config.get(DBase.dbname.name, DBase.dbname.default)
        _db[DBase.login.name] = config.get(DBase.login.name, DBase.login.default)
        _db[DBase.password.name] = config.get(DBase.password.name, DBase.password.default)
        _db[DBase.mirrors.name] = config.get(DBase.mirrors.name, DBase.mirrors.default)
        _db[DBase.default.name] = config.get(DBase.default.name, DBase.default.default)
        _db[DBase.additional.name] = config.get(DBase.additional.name, DBase.additional.default)
        _db[DBase.db.name] = config.get(DBase.db.name, DBase.db.default)
        self._dbs[_db[DBase.instance.name]] = _db

        for _filed, _cl_name in config.items():
            if _filed.startswith('cl_'):
                self._tables[_cl_name] = _db[DBase.instance.name]

        return ""

    def deleteDatabase(self) -> str:
        return ""

    def getDefaultDB(self) -> dict:
        for _db in self._dbs.values():
            if _db.get(DBase.default.name, DBase.default.default) != DBase.default.default:
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

        if _db.get(DBase.dbtype.name, DBase.dbtype.default) == dbTypes.mongo:
            return dbMongo.loadObjectFull(dbConf=_db,
                                          collection=table,
                                          idName=idName,
                                          idValue=idValue)

        return {}

    def saveItemFull(self, table: str, idName: str, idValue: str, item: dict) -> str:
        # print("save User", table, idName, idValue, item)
        _db: dict = self.getDatabaseForTable(table)

        if _db.get(DBase.dbtype.name, DBase.dbtype.default) == dbTypes.mongo:
            return dbMongo.saveObject(dbConf=_db,
                                      collection=table,
                                      idName=idName,
                                      idValue=idValue,
                                      update=item)

        return Errores.typeNotSupported.value

    def deleteItem(self, table: str, idName: str, idValue: str) -> str:
        _db: dict = self.getDatabaseForTable(table)

        if _db.get(DBase.dbtype.name, DBase.dbtype.default) == dbTypes.mongo:
            return dbMongo.deleteObject(dbConf=_db,
                                        collection=table,
                                        idName=idName,
                                        idValue=idValue)

        return Errores.typeNotSupported.value

    def loadListItems(self, table: str, filterName: str = "", filterValue: str = "") -> list:
        _db: dict = self.getDatabaseForTable(table)

        if _db.get(DBase.dbtype.name, DBase.dbtype.default) == dbTypes.mongo:
            return dbMongo.loadListItems(dbConf=_db,
                                         collection=table,
                                         filterName=filterName,
                                         filterValue=filterValue)

        return []
