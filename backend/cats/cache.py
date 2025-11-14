from django.core.cache import cache
from django_redis import get_redis_connection

CAT_LIST_CACHE_PREFIX = 'cats:list:'


def build_cat_list_cache_key(page: str) -> str:
    return f'{CAT_LIST_CACHE_PREFIX}{page}'


def reset_cat_cache() -> None:
    try:
        connection = get_redis_connection('default')
        pattern = f'{CAT_LIST_CACHE_PREFIX}*'
        for key in connection.scan_iter(pattern):
            connection.delete(key)
    except Exception:
        cache.clear()
