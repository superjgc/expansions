import datetime
from json import JSONEncoder
from typing import Union


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, datetime.timedelta):
            hour, minute, seconds = (
                obj.seconds // 3600 + obj.days * 24,
                (obj.seconds - obj.seconds // 3600 * 3600) // 60,
                obj.seconds % 60,
            )
            return "%d:%02d:%02d" % (hour, minute, seconds)
        return super(CustomJSONEncoder, self).default(obj)


class CustomUTCJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return self.__to_utc(obj).strftime("%Y-%m-%dT%H:%M:%S")
        elif isinstance(obj, datetime.date):
            return self.__to_utc(obj).strftime("%Y-%m-%d")
        elif isinstance(obj, datetime.timedelta):
            hour, minute, seconds = (
                obj.seconds // 3600 + obj.days * 24,
                (obj.seconds - obj.seconds // 3600 * 3600) // 60,
                obj.seconds % 60,
            )
            return "%d:%02d:%02d" % (hour, minute, seconds)
        elif isinstance(obj, bytes):
            # 数据库如果是blob的话, 返回的是bytes
            return obj.decode("utf8")
        return super(CustomUTCJsonEncoder, self).default(obj)

    def __to_utc(self, d: Union[datetime.datetime, datetime.date]):
        if not hasattr(self, "offset"):
            self.offset = datetime.datetime.now() - datetime.datetime.utcnow()
        return d - self.offset
