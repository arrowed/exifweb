__author__ = 'simon'

import redis

conn = redis.StrictRedis(host='127.0.0.1', port=6379, password=None)

def _add_job_to_queue(queue, job):
    key = 'queue:%s' % queue
    conn.sadd(key, job)

    return conn.scard(queue)