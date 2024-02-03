import json
import typing
from abc import ABC

from pydantic import BaseModel
from sqlalchemy import TypeDecorator, JSON


def json_model(cls: typing.Type[BaseModel]) -> typing.Type[TypeDecorator]:
    if not issubclass(cls, BaseModel):
        raise TypeError(f"Invalid type {type(cls)}, must be subclass of BaseModel")

    class Model(TypeDecorator, ABC):
        impl = JSON

        def process_bind_param(self, value, dialect):
            if isinstance(value, BaseModel):
                return value.dict()
            elif isinstance(value, (list, tuple, set)):
                return [self.process_bind_param(v, dialect) for v in value]
            elif isinstance(value, dict):
                return {k: self.process_bind_param(v, dialect) for k, v in value.items()}
            return value

        def process_result_value(self, value, dialect):
            if not value:
                return value
            elif isinstance(value, dict):
                return cls(**value)
            elif isinstance(value, str):
                return cls(**json.loads(value))
            elif isinstance(value, (list, tuple)):
                return [self.process_result_value(v, dialect) for v in value]
            raise TypeError(f"Invalid type {type(value)}, parse failed")

    return Model
