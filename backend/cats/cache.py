import logging

from django.core.cache import cache
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)

CAT_LIST_CACHE_PREFIX = 'cats:list:'


def build_cat_list_cache_key(page: str) -> str:
    return f'{CAT_LIST_CACHE_PREFIX}{page}'


def reset_cat_cache() -> None:
    pattern = f'{CAT_LIST_CACHE_PREFIX}*'
    try:
        connection = get_redis_connection('default')
        keys = list(connection.scan_iter(pattern))
        if keys:
            pipe = connection.pipeline()
            for key in keys:
                pipe.delete(key)
            pipe.execute()
    except Exception:
        logger.warning('Не удалось сбросить кэш через Redis, выполняется полная очистка')
        cache.delete_pattern(pattern)
