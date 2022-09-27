from typing import Any, Callable

from redis import Redis


class Singleton(type):
    _instances: dict = {}

    def __call__(cls, *args: tuple, **kwargs: dict) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class LocalCache(metaclass=Singleton):
    def __init__(self) -> None:
        self.storage: dict = {}

    def set(self, key: str, value: Any) -> None:
        self.storage[key] = value

    def get(self, key: str, _: Callable = None) -> Any:
        return self.storage.get(key)

    def delete(self, key: str) -> None:
        try:
            del self.storage[key]
        except KeyError:
            pass


class RedisCache(metaclass=Singleton):
    def __init__(self, redis_url: str) -> None:
        self.redis = Redis.from_url(
            redis_url,
            socket_connect_timeout=10,
            socket_keepalive=True,
            retry_on_timeout=False,
        )  # type: ignore

    def set(self, key: str, value: Any) -> None:
        self.redis.set(key, value)

    def get(self, key: str, conv: Callable = None) -> Any:
        value = self.redis.get(key)
        if value is not None and conv is not None:
            value = conv(value)

        return value

    def delete(self, key: str) -> None:
        self.redis.delete(key)
