import time

import redis
from flask import Flask

app1 = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app1.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World APP1! I have been seen {} times.\n'.format(count)
