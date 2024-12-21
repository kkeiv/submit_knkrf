import os
import json
import logging

from enum import Enum
from typing import Optional

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from libs.common import functions as fn
from libs.cache.users import CacheUsers
from storage.storage import Storage

_min_config_version_ = '1.0'


class Errores(Enum):
    NO_CONFIG = "No Config File"
    NO_CONFIG_DB = "No Database Section in Config File"
    NO_CONFIG_BOT = "No Bot Section in Config File"
    NO_CONFIG_SET = "No Settings Section in Config File"
    NO_CONFIG_LOG = "No Log Section in Config File"
    NO_VALID_VERSION = "Config has not valid version"

    NO_CL_PRICES = "No Collection 'Prices' Connection"
    NO_CL_CITIES = "No Collection 'Cities' Connection"


def default_logger(def_dir: str, tag: str) -> logging.Logger:
    _log_file_path = os.path.join(def_dir, f"{tag}.log")

    log = logging.getLogger(f'{tag}_logger')
    log.setLevel(logging.DEBUG)
    handler = logging.FileHandler(_log_file_path)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)

    return log


class Log:
    def __init__(self) -> None:
        self.dir: list = ["my_modul"]   # directory for log
        self.tag: str = "my_modul"      # tag for log
        self.size: int = 1              # size of log file in Bytes
        self.files: int = 1             # number of rotated files
        self.track: str = ""            # tracker requored

    def load(self, config: dict = {}) -> None:
        if "log" in config:
            _config = config['log']
            if "dir" in _config:
                self.dir = _config['dir']
            if "tag" in _config:
                self.tag = _config['tag']
            if "size" in _config:
                self.size = _config['size'] * 1024 * 1024
            if "files" in _config:
                self.files = _config['files']
            if "track" in _config:
                self.track = _config['track']

    def read(self) -> str:
        _ret = f"dir: {self.dir}"
        _ret = f"{_ret}, tag: {self.tag}"
        _ret = f"{_ret}, size: {self.size}"
        _ret = f"{_ret}, files: {self.files}"
        _ret = f"{{{_ret}, files: {self.track}}}"
        return _ret


class Settings:
    def __init__(self) -> None:
        self.tag: str = "my_modul"      # tag of modul

    def load(self, config: dict = {}) -> None:
        if "tag" in config:
            self.tag = config['tag']

    def read(self) -> str:
        _ret = f"{{tag: {self.tag}}}"
        return _ret


class Secrets:
    _cfg_section_ = "secrets"

    def __init__(self) -> None:
        self.tgToken: str = "your_telegram_token"               # telegram token
        self.robokassa_token: str = "your_robokassa_token"      # robokassa token
        self.ukassa_token: str = "your_ukassa_token"            # ukassa token


    def load(self, config: dict = {}) -> None:
        _pars: dict = config.get(self._cfg_section_, {})
        for _par, _val in _pars.items():
            if hasattr(self, _par):
                setattr(self, _par, _val)
            else:
                print(f"wrong param in {self._cfg_section_}: {_par}")

    def read(self) -> str:
        _ret = f"{{tgToken: {self.tgToken}}}"
        return _ret


class Subscription:
    _cfg_section_ = "subscription"

    def __init__(self) -> None:
        self.premium_period_sec: int = 0
        self.delay_sec: int = 0
        self.remainder_sec: int = 86400
        self.payment_amount_rub: int = 0
        self.payment_amount_usd: int = 0

    def load(self, config: dict = {}) -> None:
        _pars: dict = config.get(self._cfg_section_, {})
        for _par, _val in _pars.items():
            if hasattr(self, _par):
                setattr(self, _par, _val)
            else:
                print(f"wrong param in {self._cfg_section_}: {_par}")

    def read(self) -> str:
        _ret = f"{{premium_period_sec: {self.premium_period_sec}, delay_sec: {self.delay_sec}, remainder_sec: {self.remainder_sec}}}"
        return _ret


class Config:
    """A class that contains configuration data."""

    def __init__(self) -> None:
        self.is_need_stop: bool = False
        self.rootdir = os.getcwd()
        self.logger: logging.Logger = default_logger(self.rootdir, "default")
        self.tracker: logging.Logger = default_logger(self.rootdir, "def_tracker")

        self.set: Settings = Settings()
        self.secret: Secrets = Secrets()
        self.log: Log = Log()

        self.store: Storage = Storage()
        self.cu: CacheUsers = CacheUsers(self.store)
        self.scheduler = AsyncIOScheduler()
        self.tgBot: Optional[Bot] = None

        self.subscription: Subscription = Subscription()

    def load(self, config_path: str) -> bool:
        if not os.path.exists(config_path):
            print(Errores.NO_CONFIG.value)
            return False

        _config: dict = {}
        with open(config_path, 'r') as config_file:
            _config = json.load(config_file)

        if not fn.validate_version(_config.get('version', '0.0.0'), _min_config_version_):
            print(Errores.NO_VALID_VERSION.value)
            return False

        self.secret.load(_config)
        self.set.load(_config)
        self.log.load(_config)

        self.subscription.load(_config)

        for dbConf in _config:
            if dbConf.startswith('database'):
                self.store.addDatabase(_config[dbConf])
        return True

    def read(self, debug: bool = False) -> str:
        _ret = ""
        if debug:
            _ret = f"{_ret}secrets: {self.secret.read()}"
            _ret = f"{_ret}, settings: {self.set.read()}"
        else:
            _ret = f"{_ret}settings: {self.set.read()}"
        _ret = f"{_ret}, log: {self.log.read()}"
        _ret = f"{_ret}, {self.store.printForLog()}"
        return f"SETTINGS: {{{_ret}}}"


cfg: Config = Config()
