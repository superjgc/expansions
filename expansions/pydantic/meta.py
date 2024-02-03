import typing

from pydantic.main import ModelMetaclass  # noqa
from sqlalchemy import TypeDecorator

from expansions.sqlalchemy.types import json_model

__all__ = ["BaseModelMeta"]


class BaseModelMeta(ModelMetaclass):
    Type: typing.Optional[TypeDecorator] = None

    def __new__(mcs, name, bases, namespace, **kwargs):  # noqa C901
        cls = super().__new__(mcs, name, bases, namespace, **kwargs)
        cls.Type = json_model(cls)
        return cls
