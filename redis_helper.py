__author__ = 'simon'

import redis

conn = redis.StrictRedis(host='127.0.0.1', port=6379, password=None)

def _add_job_to_queue(queue, job):
    key = 'queue:%s' % queue
    conn.sadd(key, job)

    return conn.scard(key)

def _get_job_from_queue(queue):
    key = 'queue:%s' % queue
    return conn.srandmember(key)


def _processor_stream(red):
    pubsub = conn.pubsub()
    pubsub.subscribe('processor_stream')
    for message in pubsub.listen():
        yield 'retry: 50000\ndata: %s\n\n' % message['data']
