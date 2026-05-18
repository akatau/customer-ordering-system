"""
Performance utilities for API optimization and database query tuning.

Week 7 - Performance optimization and monitoring.
"""

import time
import logging
from typing import Optional, List, Any
from datetime import datetime
from functools import wraps
from sqlalchemy import event, text
from sqlalchemy.pool import Pool
from app.database import engine

logger = logging.getLogger(__name__)


class QueryProfiler:
    """Profile SQL queries to identify performance bottlenecks."""

    def __init__(self):
        """Initialize query profiler."""
        self.slow_queries = []
        self.total_queries = 0
        self.total_time = 0.0
        self.slow_query_threshold = 0.5  # 500ms

    def log_query(self, conn, cursor, statement, parameters, context, executemany):
        """
        Log query execution time (called by SQLAlchemy events).
        
        Note: This is registered as a before_cursor_execute listener.
        We store the start time in conn.info for later measurement.
        """
        conn.info.setdefault("query_start_time", []).append(time.time())

    def log_query_after(self, conn, cursor, statement, parameters, context, executemany):
        """
        Log query after execution (called by SQLAlchemy events).
        """
        total_time = time.time() - conn.info["query_start_time"].pop(-1)
        self.total_queries += 1
        self.total_time += total_time

        if total_time > self.slow_query_threshold:
            query_info = {
                "query": statement,
                "duration": total_time,
                "timestamp": datetime.now().isoformat(),
            }
            self.slow_queries.append(query_info)
            logger.warning(
                f"Slow query detected ({total_time:.3f}s): {statement[:100]}..."
            )

    def register_listeners(self):
        """Register SQLAlchemy event listeners for query profiling."""
        event.listen(
            engine.sync_engine,
            "before_cursor_execute",
            self.log_query,
        )
        event.listen(
            engine.sync_engine,
            "after_cursor_execute",
            self.log_query_after,
        )
        logger.info("Query profiler registered")

    def get_stats(self) -> dict:
        """Get query profiling statistics."""
        avg_time = (
            self.total_time / self.total_queries
            if self.total_queries > 0
            else 0
        )
        return {
            "total_queries": self.total_queries,
            "total_time": f"{self.total_time:.3f}s",
            "average_time": f"{avg_time:.3f}s",
            "slow_query_count": len(self.slow_queries),
            "slow_queries": self.slow_queries[-10:],  # Last 10
        }

    def reset(self):
        """Reset profiler statistics."""
        self.slow_queries = []
        self.total_queries = 0
        self.total_time = 0.0


# Global profiler instance
profiler = QueryProfiler()


class ConnectionPoolMonitor:
    """Monitor database connection pool health."""

    def __init__(self):
        """Initialize connection pool monitor."""
        self.max_connections = 20
        self.connection_events = []

    def on_connect(self, dbapi_conn, connection_record):
        """Called when new connection is created."""
        event_info = {
            "event": "connect",
            "timestamp": datetime.now().isoformat(),
            "pool_size": engine.sync_engine.pool.size(),
        }
        self.connection_events.append(event_info)

    def on_close(self, dbapi_conn, connection_record):
        """Called when connection is closed."""
        event_info = {
            "event": "close",
            "timestamp": datetime.now().isoformat(),
            "pool_size": engine.sync_engine.pool.size(),
        }
        self.connection_events.append(event_info)

    def register_listeners(self):
        """Register connection pool event listeners."""
        event.listen(
            engine.sync_engine,
            "connect",
            self.on_connect,
        )
        event.listen(
            engine.sync_engine,
            "close",
            self.on_close,
        )
        logger.info("Connection pool monitor registered")

    def get_stats(self) -> dict:
        """Get connection pool statistics."""
        return {
            "max_connections": self.max_connections,
            "recent_events": self.connection_events[-5:],
            "total_events": len(self.connection_events),
        }


# Global monitor instance
pool_monitor = ConnectionPoolMonitor()


def trace_performance(func):
    """
    Decorator to trace function performance.
    
    Usage:
        @trace_performance
        def some_endpoint():
            return expensive_operation()
    """

    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            if duration > 1.0:  # Log if > 1 second
                logger.warning(
                    f"Slow function: {func.__name__} took {duration:.3f}s"
                )
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                f"Function error: {func.__name__} failed after {duration:.3f}s: {e}"
            )
            raise

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            if duration > 1.0:  # Log if > 1 second
                logger.warning(
                    f"Slow function: {func.__name__} took {duration:.3f}s"
                )
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                f"Function error: {func.__name__} failed after {duration:.3f}s: {e}"
            )
            raise

    # Return appropriate wrapper
    if hasattr(func, "__await__"):
        return async_wrapper
    return sync_wrapper


class PaginationConfig:
    """Configuration for pagination."""

    def __init__(
        self,
        default_page_size: int = 20,
        max_page_size: int = 100,
        min_page_size: int = 1,
    ):
        """Initialize pagination configuration."""
        self.default_page_size = default_page_size
        self.max_page_size = max_page_size
        self.min_page_size = min_page_size

    def validate_page_size(self, page_size: Optional[int]) -> int:
        """
        Validate and normalize page size.
        
        Args:
            page_size: Requested page size or None for default
            
        Returns:
            Valid page size within configured bounds
        """
        if page_size is None:
            return self.default_page_size

        page_size = max(self.min_page_size, min(page_size, self.max_page_size))
        return page_size


# Global pagination configuration
pagination = PaginationConfig()


def paginate_query(query, skip: int = 0, limit: int = 20) -> tuple:
    """
    Apply pagination to SQLAlchemy query.
    
    Args:
        query: SQLAlchemy query object
        skip: Number of items to skip
        limit: Number of items to return
        
    Returns:
        Tuple of (total_count, paginated_results, pagination_info)
    """
    # Get total count (before limit)
    total_count = query.count()

    # Apply pagination
    results = query.offset(skip).limit(limit).all()

    # Calculate pagination info
    pagination_info = {
        "total": total_count,
        "page_size": limit,
        "current_page": (skip // limit) + 1 if limit > 0 else 1,
        "total_pages": (total_count + limit - 1) // limit if limit > 0 else 1,
        "has_next": (skip + limit) < total_count,
        "has_previous": skip > 0,
    }

    return total_count, results, pagination_info


def explain_query(query_string: str) -> str:
    """
    Get EXPLAIN plan for a query (PostgreSQL).
    
    Args:
        query_string: SQL query to explain
        
    Returns:
        EXPLAIN output showing query plan
    """
    try:
        # Note: This requires direct database connection
        # Used for query optimization analysis
        explain_query = f"EXPLAIN (ANALYZE, BUFFERS, VERBOSE) {query_string}"
        logger.debug(f"Executing EXPLAIN: {explain_query}")
        # Would need active database session to execute
        return "EXPLAIN would be executed with active session"
    except Exception as e:
        logger.error(f"Error getting query plan: {e}")
        return str(e)


# Database indexes to be added via migration
DATABASE_INDEXES = [
    {
        "table": "products",
        "columns": ["name"],
        "unique": False,
        "description": "Product name search indexing",
    },
    {
        "table": "products",
        "columns": ["category"],
        "unique": False,
        "description": "Product category filtering",
    },
    {
        "table": "products",
        "columns": ["price"],
        "unique": False,
        "description": "Product price range queries",
    },
    {
        "table": "orders",
        "columns": ["user_id", "created_at"],
        "unique": False,
        "description": "User order history queries",
    },
    {
        "table": "orders",
        "columns": ["status"],
        "unique": False,
        "description": "Order status filtering",
    },
    {
        "table": "reviews",
        "columns": ["product_id"],
        "unique": False,
        "description": "Product reviews aggregation",
    },
    {
        "table": "cart_items",
        "columns": ["user_id"],
        "unique": False,
        "description": "User cart retrieval",
    },
    {
        "table": "tickets",
        "columns": ["user_id", "status"],
        "unique": False,
        "description": "User support ticket filtering",
    },
]
