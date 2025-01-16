from typing import Dict, Any
import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)

class CachingStrategy:
    def __init__(self, default_timeout: int = 300):
        self.default_timeout = default_timeout
        
    def cache_data(self, key: str, data: Any, timeout: int = None) -> None:
        """
        Cache data with a specified key and timeout
        """
        if timeout is None:
            timeout = self.default_timeout
        cache.set(key, data, timeout)
        logger.info(f"Data cached under key: {key}")
        
    def retrieve_data(self, key: str) -> Any:
        """
        Retrieve cached data by key
        """
        data = cache.get(key)
        if data is not None:
            logger.info(f"Data retrieved from cache for key: {key}")
        else:
            logger.warning(f"No data found in cache for key: {key}")
        return data
        
    def invalidate_cache(self, key: str) -> None:
        """
        Invalidate cache entry by key
        """
        cache.delete(key)
        logger.info(f"Cache invalidated for key: {key}") 