
def listToDict(lst: list, field: str) -> dict:
    _ret: dict = {}
    for _item in lst:
        if field in _item:
            _ret[_item[field]] = _item

    return _ret


def validate_version(version: str, ethalon: str) -> bool:
    _versd = []
    for _v in version.strip().split('.'):
        if not _v.isdigit():
            return False
        else:
            _versd.append(int(_v))

    _ethsd = []
    for _e in ethalon.strip().split('.'):
        if _e == '*':
            _ethsd.append(int(999))
        elif not _e.isdigit():
            return False
        else:
            _ethsd.append(int(_e))

    for _i in range(len(_versd)):
        if _i < len(_ethsd) and _versd[_i] < _ethsd[_i]:
            return False

    return True
