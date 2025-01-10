from typing import Dict, Any, Optional, Union
import time
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass

@dataclass
class CacheEntry:
    """Represents a cached item with metadata"""
    value: Any
    expiry: float
    last_accessed: float

class CacheManager:
    """Manages caching of analysis results and calculations"""
    
    def __init__(self, default_ttl: int = 3600):
        self.cache: Dict[str, CacheEntry] = {}
        self.default_ttl = default_ttl  # Default TTL in seconds
        self.logger = logging.getLogger(__name__)
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            entry = self.cache.get(key)
            if not entry:
                return None
                
            current_time = time.time()
            
            # Check if entry has expired
            if current_time > entry.expiry:
                self.delete(key)
                return None
            
            # Update last accessed time
            entry.last_accessed = current_time
            return entry.value
            
        except Exception as e:
            self.logger.error(f"Error retrieving from cache: {str(e)}")
            return None
    
    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """Set value in cache with optional TTL"""
        try:
            current_time = time.time()
            expiry = current_time + (ttl if ttl is not None else self.default_ttl)
            
            self.cache[key] = CacheEntry(
                value=value,
                expiry=expiry,
                last_accessed=current_time
            )
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting cache value: {str(e)}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete item from cache"""
        try:
            if key in self.cache:
                del self.cache[key]
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Error deleting from cache: {str(e)}")
            return False
    
    def clear(self) -> bool:
        """Clear all items from cache"""
        try:
            self.cache.clear()
            return True
            
        except Exception as e:
            self.logger.error(f"Error clearing cache: {str(e)}")
            return False
    
    def cleanup(self, max_size: int = 1000):
        """Clean up expired entries and enforce max cache size"""
        try:
            current_time = time.time()
            
            # Remove expired entries
            expired_keys = [
                key for key, entry in self.cache.items()
                if current_time > entry.expiry
            ]
            for key in expired_keys:
                self.delete(key)
            
            # If still over max size, remove least recently accessed
            if len(self.cache) > max_size:
                sorted_entries = sorted(
                    self.cache.items(),
                    key=lambda x: x[1].last_accessed
                )
                
                # Remove oldest entries until under max size
                for key, _ in sorted_entries[:len(self.cache) - max_size]:
                    self.delete(key)
                    
        except Exception as e:
            self.logger.error(f"Error during cache cleanup: {str(e)}") 