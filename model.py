#! /usr/bin/python

import redis
import os
from urllib.parse import unquote

redis_port = os.environ['REDIS_PORT'] if 'REDIS_PORT' in os.environ else 6379
redis_client = redis.StrictRedis(host=os.environ['REDIS_HOST'], port=redis_port, db=0, decode_responses=True)

subjects = {}

def makeKey(subject):
    return 'ef:s:%s' % unquote(subject) 

def getAll():
    results = {}
    for key in redis_client.scan_iter(match="ef:s:*"):
        print(key)
        results[key.split(':')[2]] = redis_client.hgetall(key)
    print(results)
    return results

def update(subject, info):
    if not set(info.keys()).issubset(set(['engage_percent', 'engage_count', 'inject_count'])):
        return 'bad key', 500
    item = redis_client.hgetall(makeKey(subject))
    print(item)
    if not item:
        return '', 404
    redis_client.hmset(makeKey(subject), info)
    return ''

def delete(subject):
    redis_client.delete(makeKey(subject))
    return ''

def get(subject):
    item = redis_client.hgetall(makeKey(subject))
    result = {}
    for key,val in item.items():
        result[key] = float(val) if key == 'engage_percent' else int(val)
    return result

def incr(subject, engaged):
    print(engaged)
    item = get(subject)
    if not item:
        redis_client.hmset(makeKey(subject), {
            "inject_count": 1,
            "engage_count": 0,
            "engage_percent": 0
        })
    else:
        redis_client.hincrby(makeKey(subject), "inject_count", 1)
        if engaged:
            redis_client.hincrby(makeKey(subject), "engage_count", 1)

