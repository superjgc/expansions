import typing
from abc import ABC
from enum import EnumMeta, Enum

from sqlalchemy import VARCHAR, Integer
from sqlalchemy.sql.type_api import TypeEngine, TypeDecorator

__all__ = ["integer_model", "string_model"]


def _generate_model(
    cls: typing.Type[EnumMeta], impl_: typing.Type[TypeEngine]
) -> typing.Type[TypeDecorator]:
    if not issubclass(cls, Enum):
        raise TypeError(f"Invalid type {type(cls)}, must be subclass of Enum")
    if not issubclass(impl_, TypeEngine):
        raise TypeError(f"Invalid type {type(impl_)}, must be subclass of TypeEngine")

    class Model(TypeDecorator, ABC):
        impl = impl_

        def process_bind_param(self, value, dialect):
            if isinstance(value, cls):
                return value.value  # noqa
            return value

        def process_result_value(self, value, dialect):
            if value is None:
                return value
            if isinstance(value, cls):
                return value
            return cls(value)  # noqa

    return Model


def integer_model(cls: typing.Type[EnumMeta]) -> typing.Type[TypeDecorator]:
    return _generate_model(cls, Integer)


def string_model(cls: typing.Type[EnumMeta]) -> typing.Type[TypeDecorator]:
    return _generate_model(cls, VARCHAR)
