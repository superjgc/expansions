import datetime
from typing import TypeVar, Any

from humps.camel import case
from pydantic import BaseModel

from expansions.pydantic.meta import BaseModelMeta

__all__ = ["CamelModel"]

ModelType = TypeVar("ModelType", bound=BaseModel)


class CamelModel(BaseModel, metaclass=BaseModelMeta):
    """
    1. 支持只读字段
        __readonly_fields__ = ["id"], id字段只会取默认值, 赋值无效
    2. 支持只读字段继承
        __readonly_from_parent_class__ = True, 从父类继承只读字段, 父类和子类的只读字段都会生效
    3. 支持设置属性时验证
        __validate_on_set__ = True, 设置属性时进行验证, 如
        class Hello(BaseModel):
            __validate_on_set__ = True
            a: int
        hello = Hello(a=1)  # Hello(a="hello")会抛出异常, BaseModel只会在初始化时校验类型
        hello.a = "hello" # 抛出异常
    """

    __readonly_fields__ = []    # 只读字段
    __readonly_from_parent_class__ = True   # 是否从父类继承只读字段
    __validate_on_set__ = False  # 是否在设置属性时进行验证

    class Config:
        orm_mode = True  # orm对象支持BaseModel.from_orm
        arbitrary_types_allowed = True  # 允许任意类型
        alias_generator = case  # 忽略大小写与下划线, 实例化时t_t/T_T/tT/TT都可以
        allow_population_by_field_name = True  # 允许通过字段名实例化
        json_encoders = {
            datetime.datetime: (lambda obj: obj.strftime("%Y-%m-%d %H:%M:%S")),
            datetime.date: (lambda obj: obj.strftime("%Y-%m-%d")),
            datetime.timedelta: (
                lambda obj: f"{obj.seconds // 3600 + obj.days * 24}:"
                            f"{(obj.seconds - obj.seconds // 3600 * 3600) // 60}:"
                            f"{obj.seconds % 60}"
            ),
        }

    def __setattr__(self, key, value):
        if self.__validate_on_set__:
            self.validate({key: value})
        super().__setattr__(key, value)

    def __init_subclass__(cls, *args, **kwargs):
        cls.__doc__ = cls.__doc__ or ""
        super(cls).__init_subclass__()
        if not cls.__readonly_from_parent_class__:
            return

        # 获取父类的只读参数
        def _parent_class(_cls):
            for _base in _cls.__bases__:
                if _base is not object:
                    yield _base
                    yield from _parent_class(_base)

        for base in _parent_class(cls):
            if hasattr(base, "__readonly_fields__"):
                cls.__readonly_fields__ += base.__readonly_fields__
        for field_name in cls.__readonly_fields__:
            # 检查readonly field是否在fields中
            if field_name not in cls.__fields__:
                raise ValueError(f"readonly field {field_name} not in fields")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 只读参数不支持修改
        for field_name in self.__readonly_fields__:
            setattr(self, field_name, self.__fields__[field_name].default)

    @classmethod
    def from_orm(cls: ModelType, model: Any) -> ModelType:
        """
        :param model: DataModel
        :return:
        """
        return cls(**model.dict())  # noqa

    def json(self, *args, **kwargs):
        return super().json(ensure_ascii=kwargs.get("ensure_ascii", False), *args, **kwargs)
