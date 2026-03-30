import time

CACHE_TTL = 300  # seconds (5 minutes)


class SimpleCache:

    def __init__(self):
        self.store = {}

    def get(self, key):

        if key not in self.store:
            return None

        value, timestamp = self.store[key]

        if time.time() - timestamp > CACHE_TTL:
            del self.store[key]
            return None

        return value

    def set(self, key, value):

        self.store[key] = (value, time.time())


cache = SimpleCache()