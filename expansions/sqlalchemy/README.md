# types

主要用于pydantic.BaseModel解析数据库返回的数据类型, 目前支持json、整型与字符串枚举、bool,示例

```python
from pydantic import BaseModel
from sqlalchemy import Column, Integer

from expansions.sqlalchemy.types import json_model
from expansions.sqlalchemy import DataModel


# 定义数据类型
class Schema(BaseModel):
    name: str
    age: int


# 定义orm
class User(DataModel):
    id = Column(Integer, primary_key=True)
    info = Column(json_model(Schema))  # mysql column type: json


# 使用
user: User = User(info={'name': 'test', 'age': 18}).add_to_db()
print(user.info.name, user.info.age)
```

# model与query

- model: 定义了一些常用的模型, 用于快速创建orm
- query: 实现了直接打印sql与分页功能

```python
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer

from expansions.sqlalchemy import DataModel
from expansions.sqlalchemy import ExtendQuery, Pagination


# 定义orm
class User(DataModel):
    id = Column(Integer, primary_key=True)


engine = create_engine('sqlite:///:memory:', echo=True)

with sessionmaker(bind=engine)(query_cls=ExtendQuery) as session:
    DataModel.set_session(session)
    # 打印sql
    print(User.filter(User.id == 1).sql)
    # 查询
    user: User = User.filter(User.id == 1).first()
    print(user.id)
    # 分页
    users: Pagination[User] = User.filter(User.id > 1).paginate(1, 10)
    print(users.total)
    for user in users:
        print(user.id)
```