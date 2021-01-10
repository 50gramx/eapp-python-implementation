import os

import redis

redis_host = os.environ['EA_KB_REDIS_HOST']
redis_port = os.environ['EA_KB_REDIS_PORT']

redis_connector = redis.Redis(host=redis_host, port=redis_port)


def set_kv(kv_pair):
    return redis_connector.mset(kv_pair)


def get_kv(key):
    return redis_connector.get(key)


# --------------------------------
# LISTs in Redis
# --------------------------------

def rpush(list_key, item):
    return redis_connector.rpush(list_key, item)


def lrange(list_key, start, end):
    return redis_connector.lrange(list_key, start, end)


def lindex(list_key, index):
    return redis_connector.lindex(list_key, index)


def lpop(list_key):
    return redis_connector.lpop(list_key)
