import typing

from sqlalchemy.orm import Query

TABLE_VAR = typing.TypeVar("TABLE_VAR")

__all__ = ["Pagination", "ExtendQuery"]


class Pagination(typing.Generic[TABLE_VAR]):
    def __init__(
        self,
        page: int,
        per_page: int,
        total: int,
        items: typing.List[TABLE_VAR],
    ):
        self.page = page
        self.per_page = per_page
        self.total = total
        self.items = items
        self.__sql = ""

    def __iter__(self) -> typing.Iterable[TABLE_VAR]:
        return self.items.__iter__()

    @property
    def sql(self) -> str:
        return self.__sql

    @sql.setter
    def sql(self, value):
        self.__sql = value


class ExtendQuery(Query):
    def paginate(self, page=1, per_page=15) -> Pagination:
        assert page > 0
        assert per_page > 0
        query = self.limit(per_page).offset((page - 1) * per_page)

        page_res = Pagination(page, per_page, self.order_by(None).count(), query.all())
        page_res.sql = (
            self.limit(per_page)
            .offset((page - 1) * per_page)
            .statement.compile(compile_kwargs={"literal_binds": True})
        )
        return page_res

    @property
    def sql(self) -> str:
        return self.statement.compile(compile_kwargs={"literal_binds": True})

    def __str__(self):
        return self.sql

    def __repr__(self):
        return self.sql
