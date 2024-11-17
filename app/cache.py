import redis

class Cache:
    def __init__(self, redis_url="redis://localhost"):
        self.client = redis.StrictRedis.from_url(redis_url)

    def is_cached(self, title, price):
        key = f"{title}:{price}"
        return self.client.exists(key)

    def update_cache(self, title, price):
        key = f"{title}:{price}"
        self.client.set(key, "cached", ex=3600)  # Expire after 1 hour
