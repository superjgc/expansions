# 枚举功能扩展
1. 基础的功能，包括
- 判断是否在枚举定义中
- 获取所有的枚举key
- 获取所有的枚举value

2. 支持枚举类型可以被orm解析, 示例
```python
from enum import Enum
from sqlalchemy import Column, Integer

from expansions.enum import EnumIntegerMeta
from expansions.sqlalchemy import DataModel


class Status(int, Enum, metaclass=EnumIntegerMeta):
    normal = 1
    deleted = 2


# 定义orm
class User(DataModel):
    id = Column(Integer, primary_key=True)
    status = Column(Status.Type) # mysql column type: int
```