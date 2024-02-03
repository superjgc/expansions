from expansions.enum.meta import EnumBaseMeta
from expansions.sqlalchemy.types import string_model

__all__ = ["EnumStringMeta"]


class EnumStringMeta(EnumBaseMeta):
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        cls.Type = string_model(cls)  # noqa
        return cls
