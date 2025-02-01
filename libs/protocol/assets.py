from enum import Enum


class __assets__():
    DEVICES_DATA_COLLECTION = "devices_data"
    DEVICES_COLLECTION = "devices"

    DEVICES_PARAMS = ["lcd_light", "log_active", "device_type", "device_version"]


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
    par_05 = {"num": 5, "pname": "par_numbers", "type": "dec", "len": -1}
    par_10 = {"num": 10, "pname": "node_id", "type": "string", "len": 10}
    par_11 = {"num": 11, "pname": "serial", "type": "string", "len": 10}
    par_12 = {"num": 12, "pname": "device_type", "type": "dec", "len": 2}
    par_13 = {"num": 13, "pname": "device_version", "type": "dec", "len": -1}
    par_15 = {"num": 15, "pname": "lcd_light", "type": "dec", "len": 1}
    par_20 = {"num": 20, "pname": "par1", "type": "float", "len": -1}
    par_21 = {"num": 21, "pname": "par2", "type": "float", "len": -1}
    par_22 = {"num": 22, "pname": "par3", "type": "float", "len": -1}
    par_23 = {"num": 23, "pname": "par4", "type": "float", "len": -1}
    par_90 = {"num": 90, "pname": "wifi_reset", "type": "dec", "len": 1}
    par_91 = {"num": 91, "pname": "log_active", "type": "dec", "len": 1}


ParamsName: dict = {
    'par_numbers': "par_05",
    'node_id': "par_10",
    'serial': "par_11",
    'device_type': "par_12",
    'device_version': "par_13",
    'lcd_light': "par_15",
    'par1': "par_20",
    'par2': "par_21",
    'par3': "par_22",
    'par4': "par_23",
    'wifi_reset': "par_90",
    'log_active': "par_91"
}
