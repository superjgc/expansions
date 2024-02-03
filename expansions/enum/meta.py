import json
from enum import EnumMeta, Enum

__all__ = ["EnumBaseMeta"]


class EnumBaseMeta(EnumMeta):
    Type: EnumMeta = None

    def __new__(metacls, cls, bases, classdict):    # noqa
        _cls = super().__new__(metacls, cls, bases, classdict)
        # _cls.__str__ = lambda self: json.dumps(self.value)
        _cls.__repr__ = lambda self: json.dumps(self.value)
        return _cls

    def __contains__(self, item) -> bool:
        """item in EnumBaseMeta"""
        return item in self.values()

    def __str__(self) -> str:
        return json.dumps(self.dict())

    def __repr__(self) -> str:
        return self.__str__()

    def __getitem__(self, item) -> Enum:
        return self.dict()[item]

    def enum_dict(cls) -> dict:
        return cls._member_map_

    def enum_keys(cls):
        return list(cls.enum_dict().keys())

    def enum_values(cls):
        return list(cls.enum_dict().values())

    def dict(cls) -> dict:
        return {key: value.value for key, value in cls.enum_dict().items()}

    def keys(cls):
        return list(cls.dict().keys())

    def values(cls):
        return list(cls.dict().values())
