import time
from enum import Enum
from typing import Tuple

from pymongo import MongoClient
from pymongo.collection import Collection

from libs.common.config import cfg
from libs.protocol.assets import Params, ParamsPar
from libs.protocol import kProtocol55 as prot55
from libs.protocol.assets import __assets__ as _asProt_
from libs.storage.assets import DBase


class Errors(Enum):
    noError = "no_errors"
    wrongVersion = "unsupported_protocol_version"
    unknownProtocol = "unknown_protocol"
    processigError = "processing_error"
    noParamsCount = "no_parameters_count"
    noSerial = "no_serial"
    noNodeId = "no_node_id"
    wrongParamsCount = "wrong_parameters_count"


def validate_info(info: dict) -> str:
    print(1, 100, Params.par_05.value, info)
    _par_name = Params.par_05.value[ParamsPar.pname.name]
    if _par_name not in info:
        return Errors.noParamsCount.value
    _node_id = Params.par_10.value[ParamsPar.pname.name]
    if _node_id not in info:
        return Errors.noNodeId.value
    _serial = Params.par_11.value[ParamsPar.pname.name]
    if _serial not in info:
        return Errors.noSerial.value

    if info[_par_name] != (len(info) - 1):
        return Errors.wrongParamsCount.value

    return Errors.noError.value


def save_info(info: dict) -> str:

    #uri = (
    #    "mongodb://c51905_temp_knkrf_ru:KiLzuJehpiweg40@"
    #    "mongo1.c51905.h2,mongo2.c51905.h2,mongo3.c51905.h2/c51905_temp_knkrf_ru?"
    #    "replicaSet=MongoReplica"
    #)
    _db: dict = cfg.store.getDefaultDB()
    _uri = _db.get(DBase.dbtype.name, DBase.dbtype.default).value
    _uri = f"{_uri}://{_db.get(DBase.login.name, DBase.login.default)}"
    _uri = f"{_uri}:{_db.get(DBase.password.name, DBase.password.default)}"
    _uri = f"{_uri}@{','.join(_db.get(DBase.mirrors.name, DBase.mirrors.default))}"
    _uri = f"{_uri}/{_db.get(DBase.dbname.name, DBase.dbname.default)}"
    _uri = f"{_uri}?{_db.get(DBase.additional.name, DBase.additional.default)}"
    print(1, 300, _uri)

    # Connect to MongoDB server collection
    client: MongoClient = MongoClient(_uri)
    db = client[_db.get(DBase.dbname.name, DBase.dbname.default)]
    collection: Collection = db[_asProt_.DEVICES_DATA_COLLECTION.value]

    # Add new data to database
    result = collection.insert_one(info)

    return Errors.noError.value


def process_data(input: str) -> Tuple[str, dict]:
    _len = len(input)
    if _len < 2:
        return Errors.wrongVersion.value, {}

    _vals: dict = {}
    _err: str = Errors.noError.value

    _prot = input[0:2]
    if _prot == "55":
        _err, _vals = prot55.process_data(input[2:])
        if _err != prot55.Errors.noError.value:
            _err = f"{Errors.processigError.value}: {_err}"

    if _err == Errors.noError.value:
        _err = validate_info(_vals)
    _vals['time'] = int(time.time())

    if _err == Errors.noError.value:
        save_info(_vals)

    return _err, _vals
