# meta

重写了BaseModel的metaclass, 使其支持orm类型, 示例

```python
from pydantic import BaseModel
from sqlalchemy import Column, Integer

from expansions.sqlalchemy import DataModel
from expansions.pydantic.meta import BaseModelMeta


# 定义数据类型
class Schema(BaseModel, metaclass=BaseModelMeta):
    name: str
    age: int


# 定义orm
class User(DataModel):
    id = Column(Integer, primary_key=True)
    info = Column(Schema.Type)  # mysql column type: json


# 使用
user: User = User(info={'name': 'test', 'age': 18}).add_to_db()
print(user.info.name, user.info.age)
```

# camel model

常用模型, 并且定义了只读配置, 只读配置后用户传入的参数将不识别, 将使用默认参数, 示例

```python
from expansions.pydantic import CamelModel


class User(CamelModel):
    __readonly_fields__ = ["name"]

    name: str = "test"


user: User = User(name="test1")
print(user.name)  # test
```