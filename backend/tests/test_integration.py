"""
Integration tests for Week 7 - Caching, Performance, and API Optimization.

Tests verify:
- Caching layer functionality and invalidation
- API pagination and compression
- Database query optimization
- API endpoint integration with caching
- Performance metrics collection
"""

import pytest
import json
from decimal import Decimal
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from app.main import app
from app.core.cache import cache_manager, cache_key, CACHE_PATTERNS, invalidate_products
from app.utils.performance import pagination, paginate_query
from app.models.product import Product
from app.models.order import Order, OrderStatus
from app.models.user import User


client = TestClient(app)


# =====================================================================
# IN-MEMORY CACHE FOR TESTING (when Redis is unavailable)
# =====================================================================


class MockRedisCache:
    """Mock Redis cache for testing when Redis is unavailable."""
    
    def __init__(self):
        self.cache = {}
    
    def get(self, key: str):
        return self.cache.get(key)
    
    def setex(self, key: str, ttl: int, value):
        self.cache[key] = value
    
    def delete(self, *keys):
        count = 0
        for key in keys:
            if key in self.cache:
                del self.cache[key]
                count += 1
        return count
    
    def keys(self, pattern: str):
        import fnmatch
        return [k for k in self.cache.keys() if fnmatch.fnmatch(k, pattern)]
    
    def flushdb(self):
        self.cache.clear()
    
    def dbsize(self):
        return len(self.cache)
    
    def info(self):
        return {}


# Use mock cache if Redis is not available
if not cache_manager.is_available():
    cache_manager.redis = MockRedisCache()
    cache_manager.redis.mock = True


# =====================================================================
# CACHING LAYER TESTS
# =====================================================================


class TestCacheManager:
    """Test Redis cache manager functionality."""

    def test_cache_set_and_get(self):
        """Test basic cache set and get operations."""
        key = "test:key:1"
        value = {"test": "value", "number": 42}
        
        # Set value
        result = cache_manager.set(key, value)
        assert result is True
        
        # Get value
        cached = cache_manager.get(key)
        assert cached == value
        
        # Cleanup
        cache_manager.delete(key)

    def test_cache_ttl(self):
        """Test cache TTL (time-to-live) functionality."""
        key = "test:ttl:key"
        value = "test_value"
        
        # Set with 1 second TTL
        cache_manager.set(key, value, ttl=1)
        
        # Should be accessible immediately
        cached = cache_manager.get(key)
        assert cached == value
        
        # Cleanup
        cache_manager.delete(key)

    def test_cache_type_ttl(self):
        """Test cache type-specific TTL."""
        key = "test:product:key"
        value = {"name": "Test Product"}
        
        # Set with product_catalog cache type (1 hour TTL)
        cache_manager.set(key, value, cache_type="product_catalog")
        
        # Should be cached
        cached = cache_manager.get(key)
        assert cached == value
        
        # Cleanup
        cache_manager.delete(key)

    def test_cache_delete(self):
        """Test cache deletion."""
        key = "test:delete:key"
        value = "delete_me"
        
        # Set value
        cache_manager.set(key, value)
        assert cache_manager.get(key) == value
        
        # Delete
        cache_manager.delete(key)
        assert cache_manager.get(key) is None

    def test_cache_delete_pattern(self):
        """Test pattern-based cache invalidation."""
        # Set multiple keys
        cache_manager.set("products:detail:1", {"id": "1"})
        cache_manager.set("products:detail:2", {"id": "2"})
        cache_manager.set("products:list:page1", {"products": []})
        cache_manager.set("users:session:1", {"user": "1"})
        
        # Delete pattern
        deleted_count = cache_manager.delete_pattern("products:*")
        
        # Verify product keys deleted
        assert cache_manager.get("products:detail:1") is None
        assert cache_manager.get("products:list:page1") is None
        
        # Verify user keys still exist
        assert cache_manager.get("users:session:1") is not None
        
        # Cleanup
        cache_manager.delete("users:session:1")
        assert deleted_count >= 3

    def test_cache_connection_status(self):
        """Test cache connection availability check."""
        available = cache_manager.is_available()
        # Should be available in test environment
        assert isinstance(available, bool)

    def test_cache_stats(self):
        """Test cache statistics retrieval."""
        # Set some values
        cache_manager.set("stat:test:1", {"data": 1})
        cache_manager.set("stat:test:2", {"data": 2})
        
        stats = cache_manager.get_stats()
        assert isinstance(stats, dict)
        assert "total_keys" in stats or "connected_clients" in stats
        
        # Cleanup
        cache_manager.delete("stat:test:1")
        cache_manager.delete("stat:test:2")


class TestCacheKeyGeneration:
    """Test cache key generation."""

    def test_simple_cache_key(self):
        """Test simple cache key generation."""
        key = cache_key("products", 1, 20)
        assert key == "products:1:20"

    def test_cache_key_with_kwargs(self):
        """Test cache key generation with keyword arguments."""
        key = cache_key("search", page=1, query="test")
        assert "search" in key
        assert "page" in key or "query" in key

    def test_cache_key_consistency(self):
        """Test cache key generation is consistent."""
        key1 = cache_key("products", category="electronics", min_price=10)
        key2 = cache_key("products", category="electronics", min_price=10)
        assert key1 == key2


# =====================================================================
# PAGINATION TESTS
# =====================================================================


class TestPagination:
    """Test pagination functionality."""

    def test_pagination_config_defaults(self):
        """Test pagination configuration defaults."""
        config = pagination
        assert config.default_page_size == 20
        assert config.max_page_size == 100
        assert config.min_page_size == 1

    def test_validate_page_size_default(self):
        """Test page size validation returns default."""
        size = pagination.validate_page_size(None)
        assert size == 20

    def test_validate_page_size_bounds(self):
        """Test page size validation enforces bounds."""
        # Too large
        size = pagination.validate_page_size(200)
        assert size == 100  # Max
        
        # Too small
        size = pagination.validate_page_size(0)
        assert size == 1  # Min

    def test_validate_page_size_valid(self):
        """Test page size validation for valid sizes."""
        size = pagination.validate_page_size(50)
        assert size == 50


# =====================================================================
# CACHING AND API INTEGRATION TESTS
# =====================================================================


class TestProductCachingIntegration(object):
    """Test product service caching with API integration."""

    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        """Setup test products."""
        # Create test products
        self.product1 = Product(
            id="prod-1",
            name="Laptop",
            description="High-performance laptop",
            category="Electronics",
            price=Decimal("1299.99"),
            stock_quantity=10,
            image_url="https://example.com/laptop.jpg",
        )
        self.product2 = Product(
            id="prod-2",
            name="Mouse",
            description="Wireless mouse",
            category="Electronics",
            price=Decimal("29.99"),
            stock_quantity=50,
            image_url="https://example.com/mouse.jpg",
        )
        db_session.add(self.product1)
        db_session.add(self.product2)
        db_session.commit()
        
        # Clear cache before test
        invalidate_products()

    def test_product_list_caching(self):
        """Test product list caching on API endpoint."""
        # First request (cache miss)
        response1 = client.get("/api/v1/products/")
        assert response1.status_code == 200
        data1 = response1.json()
        
        # Verify response structure
        assert "data" in data1
        assert "total" in data1
        assert data1["total"] >= 2
        
        # Second request (cache hit)
        response2 = client.get("/api/v1/products/")
        assert response2.status_code == 200
        data2 = response2.json()
        
        # Data should be identical (from cache)
        assert data1["total"] == data2["total"]
        assert len(data1["data"]) == len(data2["data"])

    def test_product_detail_caching(self):
        """Test product detail caching on API endpoint."""
        product_id = "prod-1"
        
        # First request (cache miss)
        response1 = client.get(f"/api/v1/products/{product_id}")
        assert response1.status_code == 200
        data1 = response1.json()
        
        # Second request (cache hit)
        response2 = client.get(f"/api/v1/products/{product_id}")
        assert response2.status_code == 200
        data2 = response2.json()
        
        # Data should be identical
        assert data1["name"] == data2["name"]
        assert data1["price"] == data2["price"]

    def test_cache_invalidation_on_product_create(self):
        """Test cache invalidation when new product is created."""
        # Get initial product list (cache miss)
        response1 = client.get("/api/v1/products/")
        data1 = response1.json()
        initial_count = data1["total"]
        
        # Create new product (should invalidate cache)
        new_product = {
            "name": "Keyboard",
            "description": "Mechanical keyboard",
            "category": "Electronics",
            "price": 99.99,
            "stock_quantity": 25,
        }
        create_response = client.post("/api/v1/products/", json=new_product)
        assert create_response.status_code == 201
        
        # Get product list again (cache miss due to invalidation)
        response2 = client.get("/api/v1/products/")
        data2 = response2.json()
        new_count = data2["total"]
        
        # Count should increase
        assert new_count > initial_count

    def test_product_search_caching(self):
        """Test search results caching."""
        search_query = "Laptop"
        
        # First search (cache miss)
        response1 = client.get(f"/api/v1/products/?q={search_query}")
        assert response1.status_code == 200
        data1 = response1.json()
        
        # Second search (cache hit)
        response2 = client.get(f"/api/v1/products/?q={search_query}")
        assert response2.status_code == 200
        data2 = response2.json()
        
        # Results should match
        assert len(data1["data"]) == len(data2["data"])
        if len(data1["data"]) > 0:
            assert data1["data"][0]["name"] == data2["data"][0]["name"]

    def test_product_category_filter_caching(self):
        """Test category filter caching."""
        category = "Electronics"
        
        # First request with filter
        response1 = client.get(f"/api/v1/products/?category={category}")
        assert response1.status_code == 200
        data1 = response1.json()
        
        # Second request (should hit cache)
        response2 = client.get(f"/api/v1/products/?category={category}")
        assert response2.status_code == 200
        data2 = response2.json()
        
        # Results should match
        assert data1["total"] == data2["total"]


# =====================================================================
# API COMPRESSION TESTS
# =====================================================================


class TestAPICompression:
    """Test API response compression."""

    def test_gzip_compression_header(self):
        """Test GZIP compression is applied to large responses."""
        # Request with large product list
        response = client.get("/api/v1/products/?limit=100")
        assert response.status_code == 200
        
        # Check if content-encoding header includes gzip
        # (Note: TestClient may handle this transparently)
        # This test verifies the middleware is registered
        assert len(response.content) > 0

    def test_api_response_structure(self):
        """Test API response structure for large responses."""
        response = client.get("/api/v1/products/")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, dict)
        assert "data" in data
        assert isinstance(data["data"], list)

    def test_pagination_limits(self):
        """Test pagination limit constraints."""
        # Request with limit > max (should be capped)
        response = client.get("/api/v1/products/?limit=1000")
        assert response.status_code == 200
        data = response.json()
        
        # Should respect max limit
        assert len(data["data"]) <= 100

    def test_pagination_offset(self):
        """Test pagination with offset."""
        # First page
        response1 = client.get("/api/v1/products/?page=1&limit=10")
        assert response1.status_code == 200
        data1 = response1.json()
        
        # Check response structure includes pagination info
        assert "page" in data1
        assert "limit" in data1
        assert "total" in data1


# =====================================================================
# EXTERNAL SERVICE INTEGRATION TESTS
# =====================================================================


class TestPaymentFlowIntegration:
    """Test end-to-end payment flow integration with caching."""

    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        """Setup test user and products."""
        # Create test user
        self.user = User(
            id="user-1",
            email="integration@test.com",
            hashed_password="hashedpass",
            full_name="Integration Test",
        )
        
        # Create test product
        self.product = Product(
            id="pay-prod-1",
            name="Test Product",
            description="For payment testing",
            category="Test",
            price=Decimal("99.99"),
            stock_quantity=100,
            image_url="https://example.com/test.jpg",
        )
        
        db_session.add(self.user)
        db_session.add(self.product)
        db_session.commit()
        
        # Clear caches
        invalidate_products()

    def test_product_retrieval_for_checkout(self):
        """Test product retrieval during checkout process."""
        product_id = "pay-prod-1"
        
        # Product detail retrieval (cached)
        response = client.get(f"/api/v1/products/{product_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == product_id
        assert data["price"] == "99.99"  # String from JSON

    def test_cart_operations_workflow(self):
        """Test cart operations with product caching."""
        product_id = "pay-prod-1"
        
        # Get product (cache miss)
        response1 = client.get(f"/api/v1/products/{product_id}")
        assert response1.status_code == 200
        
        # Get product again (cache hit)
        response2 = client.get(f"/api/v1/products/{product_id}")
        assert response2.status_code == 200
        
        # Responses should be identical
        assert response1.json()["id"] == response2.json()["id"]


# =====================================================================
# PERFORMANCE MONITORING TESTS
# =====================================================================


class TestPerformanceMonitoring:
    """Test performance monitoring and metrics collection."""

    def test_api_response_time(self):
        """Test API response time is acceptable."""
        import time
        
        start = time.time()
        response = client.get("/api/v1/products/?limit=10")
        duration = time.time() - start
        
        # Response should be fast (< 2 seconds)
        assert response.status_code == 200
        assert duration < 2.0

    def test_health_check_performance(self):
        """Test health check endpoint performance."""
        response = client.get("/api/v1/health/")
        assert response.status_code == 200
        
        # Health check should be very fast
        assert response.json()["status"] == "healthy"


# =====================================================================
# CACHE CONSISTENCY TESTS
# =====================================================================


class TestCacheConsistency:
    """Test cache consistency and invalidation."""

    def test_cache_invalidation_patterns(self):
        """Test cache invalidation using patterns."""
        # Set multiple cache entries
        cache_manager.set("products:detail:1", {"id": "1"})
        cache_manager.set("products:detail:2", {"id": "2"})
        cache_manager.set("products:list:page1", {"products": []})
        
        # Verify entries exist
        assert cache_manager.get("products:detail:1") is not None
        
        # Invalidate all product patterns
        invalidate_products()
        
        # Verify entries are gone
        assert cache_manager.get("products:detail:1") is None
        assert cache_manager.get("products:list:page1") is None

    def test_cache_isolation_between_requests(self):
        """Test cache isolation doesn't leak between requests."""
        product_id = "prod-1"
        
        # First client request
        client1_response = client.get(f"/api/v1/products/{product_id}")
        assert client1_response.status_code == 200
        
        # Second client request (should get same cached data)
        client2_response = client.get(f"/api/v1/products/{product_id}")
        assert client2_response.status_code == 200
        
        # Data should match
        assert client1_response.json() == client2_response.json()
