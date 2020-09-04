from redis import Redis

from nostradamus.settings import REDIS_HOST, REDIS_PORT, REDIS_DB

redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


def remove_cache_record(raw_key: str, user_id: int = None) -> None:
    """ Remove cache records for all users relevant to handled key.

    Parameters
    ----------
    raw_key:
        Cache key.
    user_id:
        User id.
    """
    key_mask = f"user:*:{raw_key}"
    if user_id:
        key_mask = f"user:{user_id}:{raw_key}"

    for key in redis_conn.keys(key_mask):
        redis_conn.delete(key)


def clear_cache(raw_keys: list, user_id: int = None) -> None:
    """ Remove cache records relevant to handled keys.

    Parameters
    ----------
    raw_keys:
        Cache keys.
    user_id:
        User id.
    """
    for key in raw_keys:
        remove_cache_record(key, user_id)


def clear_page_cache(raw_keys: list, user_id: int = None) -> None:
    """ Remove cache records relevant to handled keys.

    Parameters
    ----------
    raw_keys:
        Cache keys.
    user_id:
        User id.
    """
    for key in raw_keys:
        key = f"{key}:*"
        remove_cache_record(key, user_id)
