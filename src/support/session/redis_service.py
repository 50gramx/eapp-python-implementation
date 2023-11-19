#   /*************************************************************************
#   *
#   * AMIT KUMAR KHETAN CONFIDENTIAL
#   * __________________
#   *
#   *  [2017] - [2021] Amit Kumar Khetan
#   *  All Rights Reserved.
#   *
#   * NOTICE:  All information contained herein is, and remains
#   * the property of Amit Kumar Khetan and its suppliers,
#   * if any.  The intellectual and technical concepts contained
#   * herein are proprietary to Amit Kumar Khetan
#   * and its suppliers and may be covered by U.S. and Foreign Patents,
#   * patents in process, and are protected by trade secret or copyright law.
#   * Dissemination of this information or reproduction of this material
#   * is strictly forbidden unless prior written permission is obtained
#   * from Amit Kumar Khetan.
#   */

import os

import redis

redis_host = os.environ['EA_ID_REDIS_HOST']
redis_port = os.environ['EA_ID_REDIS_PORT']

redis_connector = redis.Redis(host=redis_host, port=redis_port)


def set_kv(key, value):
    return redis_connector.mset({key: value})


def get_kv(key):
    return redis_connector.get(key).decode('utf-8')


# --------------------------------
# LISTs in Redis
# --------------------------------

def rpush(list_key, item):
    return redis_connector.rpush(list_key, str(item))


def lrange(list_key, start, end):
    return redis_connector.lrange(list_key, start, end)


def lindex(list_key, index):
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


def quick_store_list_length(list_key: str):
    return int(redis_connector.llen(list_key))
