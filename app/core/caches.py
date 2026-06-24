import asyncio
from typing import TypeVar, Generic

from cachetools import TTLCache, LRUCache

T = TypeVar("T")

class CommonCache(Generic[T]):
    def __init__(self, maxsize: int, ttl: int):
        self.cache = TTLCache(maxsize=maxsize, ttl=ttl)

    def get(self, key: str) -> T | None:
        return self.cache.get(key)

    def set(self, key: str, value: T):
        self.cache[key] = value

    def delete(self, key: str):
        self.cache.pop(key, None)

class CommonLRUCache(Generic[T]):
    def __init__(self, maxsize: int):
        self.cache = LRUCache(maxsize=maxsize)

    def get(self, key: str) -> T | None:
        return self.cache.get(key)

    def set(self, key: str, value: T):
        self.cache[key] = value

    def delete(self, key: str):
        self.cache.pop(key, None)


NONE_OBJ = object()

async def load_cache_with_lock(cache_key: str, cache_obj: CommonCache, lock_obj: asyncio.Lock, func: callable):
    result = cache_obj.get(cache_key)
    if result is not None:
        if result is NONE_OBJ:
            return None
        return result
    async with lock_obj:
        result = cache_obj.get(cache_key)
        if result is not None:
            if result is NONE_OBJ:
                return None
            return result
        result = await func()
        if result is None:
            cache_obj.set(cache_key, NONE_OBJ)
        else:
            cache_obj.set(cache_key, result)
        return result

async def load_cache(cache_key: str, cache_obj: CommonCache, func: callable):
    # 首先从缓存中加载
    result = cache_obj.get(cache_key)
    if result is not None:
        if result is NONE_OBJ:
            return None
        return result
    # 根据func获取结果
    result = await func()
    # 将结果放入缓存
    if result is None:
        cache_obj.set(cache_key, NONE_OBJ)
    else:
        cache_obj.set(cache_key, result)
    return result

verify_code_cache = CommonCache(maxsize=1024, ttl=60 * 3)
# latest_articles_cache = CommonCache(maxsize=100, ttl=60 * 30)
stat_cache = CommonCache(maxsize=10, ttl=60 * 5)
article_cache = CommonCache(maxsize=1000, ttl=60 * 5)

# 文章详情锁缓存
article_lock_cache = CommonLRUCache(maxsize=1000)
article_page_cache = CommonCache(maxsize=1000, ttl=60 * 5)
article_view_count_cache = CommonLRUCache(maxsize=1000)



