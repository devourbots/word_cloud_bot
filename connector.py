import redis
from config import REDIS_CONFIG

pool = redis.ConnectionPool(host=REDIS_CONFIG['host'], port=REDIS_CONFIG['port'], db=REDIS_CONFIG['db'],
                            encoding='utf8', decode_responses=True)


def get_connection():
    return redis.StrictRedis(connection_pool=pool)
