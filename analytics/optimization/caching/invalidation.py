from typing import List
import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)

class CacheInvalidation:
    def __init__(self):
        pass
        
    def invalidate_keys(self, keys: List[str]) -> None:
        """
        Invalidate multiple cache keys
        """
        for key in keys:
            cache.delete(key)
            logger.info(f"Cache invalidated for key: {key}")
        
    def invalidate_pattern(self, pattern: str) -> None:
        """
        Invalidate cache entries matching a pattern
        """
        # Note: This is a simplified implementation
        # In production, you would need to use your cache backend's specific
        # method for getting keys matching a pattern
        keys = [key for key in cache._cache.keys() if pattern in key]
        self.invalidate_keys(keys)
        logger.info(f"Cache invalidated for pattern: {pattern}") 