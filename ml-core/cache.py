import os
from typing import List

from redis import Redis

REDIS_HOST = os.environ.get("REDIS_HOST", default="localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", default=6379)
REDIS_DB = os.environ.get("REDIS_DB", default=0)


redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


def remove_cache_record(raw_key: str, user_id: int = None) -> None:
    """Remove cache records for all users relevant to handled key.

    :param raw_key: Cache key.
    :param user_id: User id.
    """
    key_mask = f"user:*:{raw_key}"
    if user_id:
        key_mask = f"user:{user_id}:{raw_key}"

    for key in redis_conn.keys(key_mask):
        redis_conn.delete(key)


def clear_cache(raw_keys: List[str], user_id: int = None) -> None:
    """Remove cache records relevant to handled keys.

    :param raw_keys: Cache keys.
    :param user_id: User id.
    """
    for key in raw_keys:
        remove_cache_record(key, user_id)


def clear_page_cache(raw_keys: List[str], user_id: int = None) -> None:
    """Remove cache records relevant to handled keys.

    :param raw_keys: Cache keys.
    :param user_id: User id.
    """
    for key in raw_keys:
        key = f"{key}:*"
        remove_cache_record(key, user_id)
