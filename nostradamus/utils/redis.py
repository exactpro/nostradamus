from redis import Redis

from nostradamus.settings import REDIS_HOST, REDIS_PORT, REDIS_DB

redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


def clear_cache():
    for key in redis_conn.keys("analysis_and_training:*"):
        redis_conn.delete(key)
