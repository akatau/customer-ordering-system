"""
Redis caching layer with TTL management and automatic invalidation.

Week 7 - Caching and performance optimization.
"""

import json
import redis
import logging
from datetime import datetime, timedelta
from typing import Any, Optional, Callable
from functools import wraps
from app.config import settings

logger = logging.getLogger(__name__)

# Default TTLs for different cache types
CACHE_TTLS = {
    "product_catalog": 3600,  # 1 hour
    "user_session": 86400,    # 24 hours
    "cart": 3600,              # 1 hour
    "search": 1800,            # 30 minutes
    "inventory": 1800,         # 30 minutes - for low stock alerts
    "analytics": 3600,         # 1 hour - for aggregated reports
}


class CacheManager:
    """
    Centralized Redis cache manager handling all caching operations.
    Provides TTL management and automatic invalidation for data consistency.
    """

    def __init__(self, redis_url: str = settings.redis_url):
        """Initialize Redis connection."""
        try:
            self.redis = redis.from_url(redis_url, decode_responses=True)
            # Test connection
            self.redis.ping()
            logger.info("Redis cache connected successfully")
        except redis.ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.redis = None

    def is_available(self) -> bool:
        """Check if Redis connection is available."""
        return self.redis is not None

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve value from cache.
        
        Args:
            key: Cache key to retrieve
            
        Returns:
            Cached value or None if not found
        """
        if not self.is_available():
            return None

        try:
            value = self.redis.get(key)
            if value:
                logger.debug(f"Cache hit: {key}")
                try:
                    return json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    return value
            logger.debug(f"Cache miss: {key}")
            return None
        except redis.RedisError as e:
            logger.error(f"Redis get error for key {key}: {e}")
            return None

    def set(
        self,
        key: str,
        value: Any,
        ttl: int = 3600,
        cache_type: Optional[str] = None,
    ) -> bool:
        """
        Store value in cache with TTL.
        
        Args:
            key: Cache key
            value: Value to cache (will be JSON serialized if not string)
            ttl: Time-to-live in seconds (default 1 hour)
            cache_type: Type of cache for automatic TTL selection
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_available():
            return False

        try:
            # Use cache-type-specific TTL if available
            if cache_type and cache_type in CACHE_TTLS:
                ttl = CACHE_TTLS[cache_type]

            # Serialize value
            if isinstance(value, (dict, list)):
                serialized = json.dumps(value, default=str)
            else:
                serialized = value

            self.redis.setex(key, ttl, serialized)
            logger.debug(f"Cache set: {key} (TTL: {ttl}s)")
            return True
        except redis.RedisError as e:
            logger.error(f"Redis set error for key {key}: {e}")
            return False

    def delete(self, key: str) -> bool:
        """
        Delete value from cache.
        
        Args:
            key: Cache key to delete
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_available():
            return False

        try:
            self.redis.delete(key)
            logger.debug(f"Cache deleted: {key}")
            return True
        except redis.RedisError as e:
            logger.error(f"Redis delete error for key {key}: {e}")
            return False

    def delete_pattern(self, pattern: str) -> int:
        """
        Delete all keys matching pattern (e.g., cache invalidation).
        
        Args:
            pattern: Pattern to match (e.g., "products:*")
            
        Returns:
            Number of keys deleted
        """
        if not self.is_available():
            return 0

        try:
            keys = self.redis.keys(pattern)
            if keys:
                count = self.redis.delete(*keys)
                logger.info(f"Cache invalidation: deleted {count} keys matching {pattern}")
                return count
            return 0
        except redis.RedisError as e:
            logger.error(f"Redis pattern delete error for {pattern}: {e}")
            return 0

    def clear_all(self) -> bool:
        """Clear entire cache (use carefully!)."""
        if not self.is_available():
            return False

        try:
            self.redis.flushdb()
            logger.warning("Cache cleared completely")
            return True
        except redis.RedisError as e:
            logger.error(f"Redis flush error: {e}")
            return False

    def get_stats(self) -> dict:
        """Get Redis cache statistics."""
        if not self.is_available():
            return {}

        try:
            info = self.redis.info()
            return {
                "connected_clients": info.get("connected_clients", 0),
                "used_memory": info.get("used_memory_human", "N/A"),
                "total_keys": self.redis.dbsize(),
                "evicted_keys": info.get("evicted_keys", 0),
            }
        except redis.RedisError as e:
            logger.error(f"Error getting Redis stats: {e}")
            return {}


# Global cache manager instance
cache_manager = CacheManager()


def cache_key(
    prefix: str,
    *args,
    **kwargs,
) -> str:
    """
    Generate cache key from prefix and arguments.
    
    Args:
        prefix: Cache key prefix (e.g., "products")
        *args: Positional arguments to include in key
        **kwargs: Keyword arguments to include in key
        
    Returns:
        Generated cache key
    """
    parts = [prefix]
    parts.extend(str(arg) for arg in args)
    parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
    return ":".join(parts)


def cached(
    ttl: int = 3600,
    cache_type: Optional[str] = None,
    key_prefix: Optional[str] = None,
):
    """
    Decorator to cache function results.
    
    Args:
        ttl: Time-to-live in seconds
        cache_type: Type of cache for automatic TTL lookup
        key_prefix: Custom cache key prefix (defaults to function name)
        
    Usage:
        @cached(cache_type="product_catalog")
        def get_products():
            return expensive_query()
            
        @cached(ttl=1800, key_prefix="search")
        def search_products(query: str):
            return search_db(query)
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            prefix = key_prefix or func.__name__
            key = cache_key(prefix, *args, **kwargs)

            # Try to get from cache
            cached_value = cache_manager.get(key)
            if cached_value is not None:
                return cached_value

            # Cache miss - execute function
            result = await func(*args, **kwargs)

            # Store in cache
            cache_manager.set(key, result, ttl=ttl, cache_type=cache_type)
            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            prefix = key_prefix or func.__name__
            key = cache_key(prefix, *args, **kwargs)

            # Try to get from cache
            cached_value = cache_manager.get(key)
            if cached_value is not None:
                return cached_value

            # Cache miss - execute function
            result = func(*args, **kwargs)

            # Store in cache
            cache_manager.set(key, result, ttl=ttl, cache_type=cache_type)
            return result

        # Return appropriate wrapper based on whether function is async
        if hasattr(func, "__await__"):
            return async_wrapper
        return sync_wrapper

    return decorator


def invalidate_cache(pattern: str) -> int:
    """
    Invalidate cache entries matching pattern.
    
    Args:
        pattern: Pattern to match (e.g., "products:*")
        
    Returns:
        Number of keys deleted
    """
    return cache_manager.delete_pattern(pattern)


# Cache key patterns for invalidation
CACHE_PATTERNS = {
    "product_list": "products:list:*",
    "product_detail": "products:detail:*",
    "search_results": "search:*",
    "user_cart": "cart:user:*",
    "user_session": "session:user:*",
    "inventory_low": "inventory:low:*",
}


def invalidate_products():
    """Invalidate all product-related caches."""
    count = 0
    count += invalidate_cache(CACHE_PATTERNS["product_list"])
    count += invalidate_cache(CACHE_PATTERNS["product_detail"])
    count += invalidate_cache(CACHE_PATTERNS["search_results"])
    logger.info(f"Invalidated product caches: {count} entries")


def invalidate_user_cart(user_id: str):
    """Invalidate cart cache for specific user."""
    pattern = f"cart:user:{user_id}:*"
    count = invalidate_cache(pattern)
    logger.info(f"Invalidated cart cache for user {user_id}: {count} entries")


def invalidate_inventory():
    """Invalidate all inventory-related caches."""
    count = invalidate_cache(CACHE_PATTERNS["inventory_low"])
    logger.info(f"Invalidated inventory caches: {count} entries")
