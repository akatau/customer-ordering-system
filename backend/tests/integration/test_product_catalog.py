"""
QA Sprint Week 7: Product Catalog Integration Tests
Tests for product browsing, search, and filtering
"""

import pytest
from decimal import Decimal

class TestProductCatalog:
    """Test product catalog functionality"""
    
    def test_product_listing(self, db_session, sample_products):
        """Test listing all products"""
        from app.services.product_service import list_products
        
        products = list_products(db_session)
        
        assert len(products) > 0
        assert len(products) == len(sample_products)
    
    def test_product_pagination(self, db_session, sample_products):
        """Test product pagination"""
        from app.services.product_service import list_products
        
        page1 = list_products(db_session, skip=0, limit=5)
        page2 = list_products(db_session, skip=5, limit=5)
        
        assert len(page1) <= 5
        assert len(page2) <= 5
    
    def test_product_retrieval_by_id(self, db_session, sample_product):
        """Test retrieving product by ID"""
        from app.services.product_service import get_product
        
        product = get_product(db_session, sample_product.id)
        
        assert product is not None
        assert product.id == sample_product.id
        assert product.name == sample_product.name
    
    def test_product_not_found(self, db_session):
        """Test product not found"""
        from app.services.product_service import get_product
        from app.exceptions import NotFoundError
        
        with pytest.raises(NotFoundError):
            get_product(db_session, 99999)


class TestProductSearch:
    """Test product search functionality"""
    
    def test_search_by_name(self, db_session, sample_products):
        """Test searching products by name"""
        from app.services.product_service import search_products
        
        results = search_products(db_session, query="Laptop")
        
        assert len(results) > 0
        assert any("Laptop" in p.name for p in results)
    
    def test_search_case_insensitive(self, db_session, sample_products):
        """Test case-insensitive search"""
        from app.services.product_service import search_products
        
        results_upper = search_products(db_session, query="LAPTOP")
        results_lower = search_products(db_session, query="laptop")
        
        assert len(results_upper) == len(results_lower)
    
    def test_search_by_description(self, db_session, sample_products):
        """Test searching in product description"""
        from app.services.product_service import search_products
        
        results = search_products(db_session, query="portable")
        
        assert len(results) > 0
    
    def test_search_no_results(self, db_session):
        """Test search with no results"""
        from app.services.product_service import search_products
        
        results = search_products(db_session, query="nonexistentproduct")
        
        assert len(results) == 0


class TestProductFiltering:
    """Test product filtering"""
    
    def test_filter_by_category(self, db_session, sample_products):
        """Test filtering by category"""
        from app.services.product_service import filter_products
        
        results = filter_products(db_session, category="Electronics")
        
        assert len(results) > 0
        assert all(p.category == "Electronics" for p in results)
    
    def test_filter_by_price_range(self, db_session, sample_products):
        """Test filtering by price range"""
        from app.services.product_service import filter_products
        
        results = filter_products(
            db_session,
            min_price=Decimal("100.00"),
            max_price=Decimal("1000.00")
        )
        
        assert all(
            Decimal("100.00") <= p.price <= Decimal("1000.00")
            for p in results
        )
    
    def test_filter_by_availability(self, db_session, sample_products):
        """Test filtering by availability"""
        from app.services.product_service import filter_products
        
        results = filter_products(db_session, in_stock=True)
        
        assert all(p.stock > 0 for p in results)
    
    def test_filter_by_rating(self, db_session, sample_products):
        """Test filtering by minimum rating"""
        from app.services.product_service import filter_products
        
        results = filter_products(db_session, min_rating=4.0)
        
        assert all(p.average_rating >= 4.0 for p in results)
    
    def test_combined_filters(self, db_session, sample_products):
        """Test combining multiple filters"""
        from app.services.product_service import filter_products
        
        results = filter_products(
            db_session,
            category="Electronics",
            min_price=Decimal("100.00"),
            max_price=Decimal("1000.00"),
            in_stock=True,
            min_rating=3.5
        )
        
        assert len(results) > 0


class TestProductSorting:
    """Test product sorting"""
    
    def test_sort_by_price_ascending(self, db_session, sample_products):
        """Test sorting by price ascending"""
        from app.services.product_service import list_products
        
        products = list_products(db_session, sort_by="price", sort_order="asc")
        
        prices = [p.price for p in products]
        assert prices == sorted(prices)
    
    def test_sort_by_price_descending(self, db_session, sample_products):
        """Test sorting by price descending"""
        from app.services.product_service import list_products
        
        products = list_products(db_session, sort_by="price", sort_order="desc")
        
        prices = [p.price for p in products]
        assert prices == sorted(prices, reverse=True)
    
    def test_sort_by_rating(self, db_session, sample_products):
        """Test sorting by rating"""
        from app.services.product_service import list_products
        
        products = list_products(db_session, sort_by="rating", sort_order="desc")
        
        ratings = [p.average_rating for p in products]
        assert ratings == sorted(ratings, reverse=True)
    
    def test_sort_by_newest(self, db_session, sample_products):
        """Test sorting by creation date"""
        from app.services.product_service import list_products
        
        products = list_products(db_session, sort_by="created_at", sort_order="desc")
        
        dates = [p.created_at for p in products]
        assert dates == sorted(dates, reverse=True)


class TestProductDetails:
    """Test product details"""
    
    def test_product_has_all_attributes(self, db_session, sample_product):
        """Test product has all required attributes"""
        assert hasattr(sample_product, "id")
        assert hasattr(sample_product, "name")
        assert hasattr(sample_product, "description")
        assert hasattr(sample_product, "price")
        assert hasattr(sample_product, "stock")
        assert hasattr(sample_product, "category")
    
    def test_product_images(self, db_session, sample_product_with_images):
        """Test product images"""
        assert len(sample_product_with_images.images) > 0
        assert all(img.url for img in sample_product_with_images.images)
    
    def test_product_reviews(self, db_session, sample_product_with_reviews):
        """Test product reviews"""
        assert len(sample_product_with_reviews.reviews) > 0
        assert all(0 <= r.rating <= 5 for r in sample_product_with_reviews.reviews)


class TestProductReviews:
    """Test product reviews functionality"""
    
    def test_add_product_review(self, db_session, customer_user, sample_product):
        """Test adding a product review"""
        from app.services.product_service import add_review
        
        review = add_review(
            db_session,
            product_id=sample_product.id,
            user_id=customer_user.id,
            rating=5,
            comment="Great product!"
        )
        
        assert review.rating == 5
        assert review.comment == "Great product!"
    
    def test_review_rating_validation(self, db_session, customer_user, sample_product):
        """Test review rating validation"""
        from app.services.product_service import add_review
        from app.exceptions import ValidationError
        
        with pytest.raises(ValidationError):
            add_review(
                db_session,
                product_id=sample_product.id,
                user_id=customer_user.id,
                rating=10,  # Invalid: > 5
            )
    
    def test_update_product_average_rating(self, db_session, sample_product):
        """Test product average rating calculation"""
        from app.services.product_service import add_review, update_product_rating
        
        # Add reviews with different ratings
        add_review(
            db_session,
            product_id=sample_product.id,
            user_id=1,
            rating=5,
        )
        add_review(
            db_session,
            product_id=sample_product.id,
            user_id=2,
            rating=3,
        )
        
        update_product_rating(db_session, sample_product.id)
        
        # Average should be 4
        assert sample_product.average_rating == 4.0
    
    def test_list_product_reviews(self, db_session, sample_product_with_reviews):
        """Test listing product reviews"""
        from app.services.product_service import get_reviews
        
        reviews = get_reviews(db_session, sample_product_with_reviews.id)
        
        assert len(reviews) > 0


class TestProductInventory:
    """Test product inventory management"""
    
    def test_product_stock_decreases_on_order(self, db_session, sample_product):
        """Test stock decreases when order is placed"""
        initial_stock = sample_product.stock
        
        from app.services.inventory_service import decrease_stock
        decrease_stock(db_session, sample_product.id, 2)
        
        assert sample_product.stock == initial_stock - 2
    
    def test_stock_cannot_go_negative(self, db_session, sample_product):
        """Test stock cannot go below zero"""
        from app.services.inventory_service import decrease_stock
        from app.exceptions import InsufficientStockError
        
        with pytest.raises(InsufficientStockError):
            decrease_stock(db_session, sample_product.id, sample_product.stock + 10)
    
    def test_reserve_stock(self, db_session, sample_product):
        """Test reserving stock"""
        from app.services.inventory_service import reserve_stock
        
        reserved = reserve_stock(db_session, sample_product.id, 2)
        
        assert reserved.quantity == 2
    
    def test_release_reserved_stock(self, db_session, sample_product):
        """Test releasing reserved stock"""
        from app.services.inventory_service import reserve_stock, release_stock
        
        reservation = reserve_stock(db_session, sample_product.id, 2)
        release_stock(db_session, reservation.id)
        
        assert reservation.is_released is True


class TestProductVisibility:
    """Test product visibility"""
    
    def test_hidden_products_not_listed(self, db_session):
        """Test hidden products are not visible"""
        from app.models import Product
        from app.services.product_service import list_products
        
        visible_product = Product(
            name="Visible",
            price=Decimal("100.00"),
            is_active=True,
        )
        hidden_product = Product(
            name="Hidden",
            price=Decimal("100.00"),
            is_active=False,
        )
        
        db_session.add(visible_product)
        db_session.add(hidden_product)
        db_session.commit()
        
        products = list_products(db_session)
        
        assert any(p.name == "Visible" for p in products)
        assert not any(p.name == "Hidden" for p in products)
    
    def test_admin_can_see_all_products(self, db_session, admin_user):
        """Test admin can see inactive products"""
        from app.services.product_service import list_products
        
        products = list_products(db_session, include_inactive=True)
        
        assert len(products) > 0
