from django.core.cache import cache
from functools import wraps
import hashlib
import json

class CacheManager:
    @staticmethod
    def cache_key(prefix: str, *args, **kwargs) -> str:
        """Generate a unique cache key"""
        key_parts = [prefix]
        key_parts.extend([str(arg) for arg in args])
        if kwargs:
            key_parts.append(hashlib.md5(
                json.dumps(kwargs, sort_keys=True).encode()
            ).hexdigest())
        return ':'.join(key_parts)

    @staticmethod
    def cache_decorator(prefix: str, timeout: int = 300):
        """Decorator for caching function results"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                cache_key = CacheManager.cache_key(prefix, *args, **kwargs)
                result = cache.get(cache_key)
                
                if result is None:
                    result = await func(*args, **kwargs)
                    cache.set(cache_key, result, timeout)
                
                return result
            return wrapper
        return decorator

# Usage example in views
@CacheManager.cache_decorator('feed', 300)
async def get_feed(profile_id: str, page: int = 1):
    return await feed_algorithm.get_personalized_feed(profile_id, page) 