from typing import Any


class Parameter():
    name = "name_def"
    value = "value_def"
    kind: type = str
    default = "default_def"

    def __init__(self, name: str, kind: type, default: Any, value: Any = None) -> None:
        self.name = name
        self.kind = kind
        self.default = default
        self.value = value

    def __repr__(self):
        return f"Parameter(name='{self.name}', kind={self.kind.__name__}, default={self.default}, value={self.value})"
