import functools
import time
from ..core.logger import logger

def simple_cache(ttl_seconds: int = 300):
    """
    Decorator for simple in-memory caching with TTL.
    """
    def decorator(func):
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            now = time.time()
            
            if key in cache:
                result, timestamp = cache[key]
                if now - timestamp < ttl_seconds:
                    logger.debug(f"Cache hit for {func.__name__}")
                    return result
            
            logger.debug(f"Cache miss for {func.__name__}")
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
            
        return wrapper
    return decorator
