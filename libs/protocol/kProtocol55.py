from enum import Enum
from typing import Tuple

from libs.protocol.assets import Params, ParamsPar, ParamsType


class Errors(Enum):
    noError = "no_errors"
    unknownParameter = "unknown_parameter"


class ParamsErrors(Enum):
    noError = 0
    headerLen = -1
    valueLen = -2
    unknownPar = -3
    unexpectelLen = -4
    unexpectedType = -5


def process_parameter(inData: str, params: dict) -> int:
    _len = len(inData)
    if _len < 4:
        return ParamsErrors.headerLen.value

    _par_raw = inData[0:2]
    _val_len = int(inData[2:4])
    _ret_val = 4 + _val_len

    if _len < _ret_val:
        return ParamsErrors.valueLen.value

    _par = f"par_{_par_raw}"
    if _par in Params._member_names_:
        _expected_par = getattr(Params, _par).value
        _expected_len = _expected_par.get(ParamsPar.len.name, 0)
        _expected_type = _expected_par.get(ParamsPar.type.name, ParamsType)
        _par_name = _expected_par.get(ParamsPar.pname.name, "unknown")
        _value = inData[4:_ret_val]

        if _expected_len > 0 and _expected_len != _val_len:
            return ParamsErrors.unexpectelLen.value

        if _expected_type == ParamsType.dec.value:
            params[_par_name] = int(_value)
        elif _expected_type == ParamsType.float.value:
            params[_par_name] = float(_value)
        elif _expected_type == ParamsType.string.value:
            params[_par_name] = _value
        else:
            return ParamsErrors.unexpectedType.value
    else:
        return ParamsErrors.unknownPar.value

    return _ret_val


def process_data(data: str) -> Tuple[str, dict]:
    _ret: dict = {}
    _buf = data
    _err = ""

    while len(_buf) > 0 and _err == "":
        _parLen = process_parameter(_buf, _ret)
        if _parLen > 0:
            _buf = _buf[_parLen:]
        else:
            _err = Errors.unknownParameter.value

    if _err != "":
        return f"Params error: {_err}", {}

    return Errors.noError.value, _ret
