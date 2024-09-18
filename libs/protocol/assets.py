from enum import Enum


class ParamsPar(Enum):
    num = -1
    pname = "unuse"
    type = "unknown"
    len = 0


class ParamsType(Enum):
    dec = "dec"
    float = "float"
    string = "string"

    unknown = "unknown"


class Params(Enum):
    par_05 = {"num": 5, "pname": "par_numbers", "type": "dec", "len": 2}
    par_10 = {"num": 10, "pname": "node_id", "type": "dec", "len": 10}
    par_11 = {"num": 11, "pname": "serial", "type": "string", "len": 10}
    par_12 = {"num": 12, "pname": "device_type", "type": "dec", "len": 2}
    par_13 = {"num": 13, "pname": "device_version", "type": "dec", "len": -1}
    par_20 = {"num": 20, "pname": "par1", "type": "float", "len": -1}
    par_21 = {"num": 21, "pname": "par2", "type": "float", "len": -1}
    par_22 = {"num": 22, "pname": "par3", "type": "float", "len": -1}
    par_23 = {"num": 23, "pname": "par4", "type": "float", "len": -1}
