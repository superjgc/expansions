from typing import TypeVar, Union
from pydantic import BaseModel
from sqlalchemy.orm import as_declarative, Session, declared_attr, Query

from expansions.sqlalchemy.query import ExtendQuery
from expansions.utils.case import to_camel, to_underline

__all__ = ["DataModel"]

from expansions.utils.common import classproperty

ModelType = TypeVar("ModelType")


@as_declarative()
class DataModel:
    def __init__(self, *args, **kwargs):
        ...

    @classmethod
    def session(cls) -> Session:
        """
        with sessionmaker(bind=engine)(query_cls=ExtendQuery) as session:
            DataModel.session = classmethod(lambda cls: your_session)
        """
        ...

    @declared_attr
    def __tablename__(cls) -> str:  # noqa
        return to_underline(cls.__name__)

    @classproperty
    def columns(cls):   # noqa
        return [column.name for column in cls.__table__.columns]

    @classmethod
    def query(cls, *args) -> Union[ExtendQuery, Query]:
        if not args:
            return cls.session().query(cls)
        return cls.session().query(*args)

    @classmethod
    def filter(cls, *args) -> ExtendQuery:
        return cls.session().query(cls).filter(*args)

    @classmethod
    def commit(cls):
        cls.session().commit()

    @classmethod
    def rollback(cls):
        cls.session().rollback()

    def add_to_db(self, auto_commit=True):
        self.session().add(self)
        if auto_commit:
            self.session().commit()
        self.session().flush([self])
        return self

    def delete_from_db(self, auto_commit=True):
        self.session().delete(self)
        if not auto_commit:
            return
        self.session().commit()

    def dict(self, camel=False, cap=False) -> dict:
        data = {}
        for column in self.__table__.columns:
            key = column.name
            value = getattr(self, key)
            if issubclass(value.__class__, BaseModel):
                data[key if not camel else to_camel(key, cap)] = value.dict()
                continue
            data[key if not camel else to_camel(key, cap)] = value
        return data

    def camel_dict(self, cap=False) -> dict:
        return self.to_dict(camel=True, cap=cap)
