import os

import redis

redis_host = os.environ['EA_CONVERSATION_REDIS_HOST']
redis_port = os.environ['EA_CONVERSATION_REDIS_PORT']

redis_connector = redis.Redis(host=redis_host, port=redis_port)


def get_redis_connector():
    return redis_connector


def set_kv(key, value):
    return redis_connector.mset({key: value})


def get_kv(key):
    return redis_connector.get(key).decode('utf-8')


# --------------------------------
# LISTs in Redis
# --------------------------------

# --------------------------------
# LISTs in Redis
# --------------------------------

def rpush(list_key, item):
    return redis_connector.rpush(list_key, str(item))


def lindex(list_key, index):
    value = redis_connector.lindex(list_key, index)
    return value if value is None else value.decode('utf-8')


def lrange(list_key, start, end):
    return redis_connector.lrange(list_key, start, end)


def quick_store_get_item_from_list_with_index(list_key, index):
    value = redis_connector.lindex(list_key, index)
    return value if value is None else value.decode('utf-8')


def lpop(list_key):
    value = redis_connector.lpop(list_key)
    return value if value is None else value.decode('utf-8')


def quick_store_list_pop_all_items(list_key: str):
    popped_items = []
    for counter in range(quick_store_list_length(list_key)):
        popped_items.append(redis_connector.lpop(name=list_key))
    return popped_items


def quick_store_delete_list(list_key: str):
    return redis_connector.delete(list_key)


def quick_store_list_length(list_key: str):
    return int(redis_connector.llen(list_key))
