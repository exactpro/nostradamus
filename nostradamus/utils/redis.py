from redis import Redis

from nostradamus.settings import REDIS_HOST, REDIS_PORT, REDIS_DB

redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


def clear_cache(raw_key: str):
    for key in redis_conn.keys(f"{raw_key}:*"):
        redis_conn.delete(key)


def clear_cache_by_keys(raw_keys: list):
    for key in raw_keys:
        clear_cache(key)
