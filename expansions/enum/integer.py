from expansions.enum.meta import EnumBaseMeta
from expansions.sqlalchemy.types import integer_model

__all__ = ["EnumIntegerMeta"]


class EnumIntegerMeta(EnumBaseMeta):
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        cls.Type = integer_model(cls)  # noqa
        return cls
