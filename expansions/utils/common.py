import os
import socket


class classproperty(property):  # noqa
    """
    class Test:
        @classproperty
        def a(cls):
            return cls.__name__

    print(Test.a) -> Test
    print(Test().a) -> Test
    """

    def __get__(self, instance, owner):  # noqa
        return classmethod(self.fget).__get__(None, owner)()


class UnsafeDict(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            return None

    def __setattr__(self, name, value):
        self[name] = value


def local_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(('10.255.255.255', 1))
        ip = sock.getsockname()[0]
    except Exception as _:  # noqa
        ip = '127.0.0.1'
    finally:
        sock.close()
    return ip


def dir_create_if_not_exists(path: str):
    if not os.path.exists(path):
        os.makedirs(path)
    return path
