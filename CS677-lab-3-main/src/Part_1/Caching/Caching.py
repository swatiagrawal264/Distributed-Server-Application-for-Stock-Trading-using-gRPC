import time

# Initialize a new Cache object with an empty dictionary to store key-value pairs,
# a maximum size for the cache, and a time-to-live (TTL) value for cache entries.
class Cache:
    def __init__(self, max_size=100, ttl=60):
        self.cache = {}
        self.max_size = max_size
        self.ttl = ttl

# Retrieve a value from the cache given a key.
# If the key is not in the cache, return None.
    def get(self, key):
        if key not in self.cache:
            return None


# Get the value and timestamp associated with the key.
        value, timestamp = self.cache[key]
        
        
# If the value has expired (i.e., its timestamp is older than the TTL), delete the entry
#from the cache and return None.
        if time.time() - timestamp > self.ttl:
            del self.cache[key]
            return None
# Otherwise, return the value.
        return value


# Insert a new key-value pair into the cache.
# If the cache has reached its maximum size, remove the oldest entry to make room for the new one.
    def put(self, key, value):
        if len(self.cache) >= self.max_size:
            self.cache.pop(next(iter(self.cache)))
            
            
# Add the new key-value pair to the cache with a timestamp equal to the current time.
        self.cache[key] = (value, time.time())


# Delete a key-value pair from the cache given a key.
        # If the key is not in the cache, do nothing.
    def delete(self, key):
        if key in self.cache:
            del self.cache[key]
