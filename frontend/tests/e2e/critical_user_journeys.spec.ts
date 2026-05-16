"""
QA Sprint Week 7: E2E Critical User Journey Tests
Tests for critical user workflows and integration
"""

import pytest
from playwright.sync_api import sync_playwright, expect


class TestCustomerJourneys:
    """Test critical customer user journeys"""
    
    def test_registration_login_browse_journey(self, page, base_url):
        """Test: User Registration → Login → Browse Products"""
        # Register new user
        page.goto(f"{base_url}/register")
        page.fill('input[name="email"]', "testuser@example.com")
        page.fill('input[name="password"]', "SecurePassword123!")
        page.fill('input[name="firstName"]', "Test")
        page.fill('input[name="lastName"]', "User")
        page.click('button:has-text("Register")')
        
        # Verify registration success
        expect(page).to_have_url(f"{base_url}/login")
        
        # Login
        page.fill('input[name="email"]', "testuser@example.com")
        page.fill('input[name="password"]', "SecurePassword123!")
        page.click('button:has-text("Login")')
        
        # Verify logged in
        expect(page).to_have_url(f"{base_url}/home")
        expect(page.locator("text=Welcome, Test")).to_be_visible()
        
        # Browse products
        page.click('a:has-text("Products")')
        expect(page).to_have_url(f"{base_url}/products")
        
        # Verify products loaded
        expect(page.locator(".product-item")).to_have_count_greater_than(0)
    
    def test_product_search_filter_journey(self, page, base_url):
        """Test: Product Search → Filter → View Details"""
        page.goto(f"{base_url}/products")
        
        # Search for products
        page.fill('input[placeholder="Search products..."]', "laptop")
        page.click('button:has-text("Search")')
        
        # Filter by price
        page.click('text=Filter')
        page.fill('input[name="minPrice"]', "500")
        page.fill('input[name="maxPrice"]', "1500")
        page.click('button:has-text("Apply Filters")')
        
        # Verify filtered results
        products = page.locator(".product-item")
        for product in products.all():
            price_text = product.locator(".product-price").text_content()
            price = float(price_text.replace("$", ""))
            assert 500 <= price <= 1500
        
        # Click on first product
        page.click(".product-item >> nth=0")
        
        # Verify product details
        expect(page).to_have_url_matching(r"/products/\d+")
        expect(page.locator(".product-title")).to_be_visible()
        expect(page.locator(".product-description")).to_be_visible()
    
    def test_add_to_cart_checkout_journey(self, page, base_url, logged_in_customer):
        """Test: Add to Cart → Checkout → Payment"""
        page.goto(f"{base_url}/products")
        
        # Add product to cart
        page.click(".product-item >> nth=0")
        page.fill('input[name="quantity"]', "2")
        page.click('button:has-text("Add to Cart")')
        
        # Verify cart updated
        expect(page.locator(".cart-badge")).to_contain_text("2")
        
        # Go to cart
        page.click('a:has-text("Cart")')
        expect(page).to_have_url(f"{base_url}/cart")
        
        # Verify items in cart
        expect(page.locator(".cart-item")).to_have_count(1)
        
        # Proceed to checkout
        page.click('button:has-text("Checkout")')
        expect(page).to_have_url(f"{base_url}/checkout")
        
        # Fill shipping address
        page.fill('input[name="street"]', "123 Main St")
        page.fill('input[name="city"]', "New York")
        page.fill('input[name="state"]', "NY")
        page.fill('input[name="zip"]', "10001")
        page.click('button:has-text("Continue to Payment")')
        
        # Fill payment information
        page.frame_locator('iframe[title="Stripe"]').locator('input[name="cardnumber"]').fill("4111111111111111")
        page.frame_locator('iframe[title="Stripe"]').locator('input[name="exp-date"]').fill("12/25")
        page.frame_locator('iframe[title="Stripe"]').locator('input[name="cvc"]').fill("123")
        
        # Place order
        page.click('button:has-text("Place Order")')
        
        # Verify order confirmation
        expect(page).to_have_url_matching(r"/order-confirmation/\d+")
        expect(page.locator("text=Order Confirmed")).to_be_visible()
    
    def test_order_tracking_journey(self, page, base_url, logged_in_customer):
        """Test: Order Confirmation → Tracking"""
        # Navigate to orders
        page.goto(f"{base_url}/orders")
        
        # Click on first order
        page.click(".order-item >> nth=0")
        
        # Verify order details
        expect(page).to_have_url_matching(r"/orders/\d+")
        expect(page.locator(".order-status")).to_be_visible()
        
        # Verify tracking information
        tracking_number = page.locator(".tracking-number").text_content()
        assert tracking_number is not None
        
        # Click track shipment
        page.click('button:has-text("Track Shipment")')
        
        # Verify tracking page
        expect(page).to_have_url_matching(r"/track/")
        expect(page.locator(".tracking-timeline")).to_be_visible()


class TestAdminJourneys:
    """Test critical admin user journeys"""
    
    def test_admin_product_management_journey(self, page, base_url, logged_in_admin):
        """Test: Admin Product Management"""
        page.goto(f"{base_url}/admin/products")
        expect(page).to_have_url(f"{base_url}/admin/products")
        
        # Add new product
        page.click('button:has-text("Add Product")')
        expect(page).to_have_url(f"{base_url}/admin/products/new")
        
        # Fill product form
        page.fill('input[name="name"]', "New Product")
        page.fill('textarea[name="description"]', "Test product description")
        page.fill('input[name="price"]', "99.99")
        page.fill('input[name="stock"]', "100")
        page.select_option('select[name="category"]', "Electronics")
        page.click('button:has-text("Save Product")')
        
        # Verify product created
        expect(page).to_have_url(f"{base_url}/admin/products")
        expect(page.locator("text=Product created successfully")).to_be_visible()
        
        # Verify new product in list
        expect(page.locator("text=New Product")).to_be_visible()
    
    def test_admin_order_management_journey(self, page, base_url, logged_in_admin):
        """Test: Admin Order Management"""
        page.goto(f"{base_url}/admin/orders")
        
        # Click on first order
        page.click(".order-item >> nth=0")
        
        # Update order status
        page.select_option('select[name="status"]', "shipped")
        page.click('button:has-text("Update Status")')
        
        # Verify status updated
        expect(page.locator("text=Order updated successfully")).to_be_visible()
        expect(page.locator(".order-status")).to_contain_text("Shipped")
    
    def test_admin_user_management_journey(self, page, base_url, logged_in_admin):
        """Test: Admin User Management"""
        page.goto(f"{base_url}/admin/users")
        
        # Search for user
        page.fill('input[placeholder="Search users..."]', "test@example.com")
        page.click('button:has-text("Search")')
        
        # Verify user found
        expect(page.locator(".user-item")).to_have_count_greater_than(0)
        
        # Click on user
        page.click(".user-item >> nth=0")
        
        # View user details
        expect(page).to_have_url_matching(r"/admin/users/\d+")
        expect(page.locator(".user-email")).to_be_visible()


class TestSupportJourneys:
    """Test critical support user journeys"""
    
    def test_support_ticket_creation_journey(self, page, base_url, logged_in_customer):
        """Test: Support Ticket Creation"""
        page.goto(f"{base_url}/support/tickets")
        
        # Create new ticket
        page.click('button:has-text("Create Ticket")')
        
        # Fill ticket form
        page.fill('input[name="subject"]', "Product Defect")
        page.select_option('select[name="category"]', "Product Quality")
        page.fill('textarea[name="description"]', "The product arrived with defects")
        page.click('button:has-text("Submit")')
        
        # Verify ticket created
        expect(page).to_have_url_matching(r"/support/tickets/\d+")
        expect(page.locator("text=Ticket created successfully")).to_be_visible()
    
    def test_support_ticket_resolution_journey(self, page, base_url, logged_in_support):
        """Test: Support Ticket Resolution"""
        page.goto(f"{base_url}/admin/support/tickets")
        
        # Filter open tickets
        page.select_option('select[name="status"]', "open")
        page.click('button:has-text("Filter")')
        
        # Click on first ticket
        page.click(".ticket-item >> nth=0")
        
        # Add response
        page.fill('textarea[name="response"]', "We will send a replacement")
        page.click('button:has-text("Send Response")')
        
        # Update ticket status
        page.select_option('select[name="status"]', "resolved")
        page.click('button:has-text("Update")')
        
        # Verify ticket resolved
        expect(page.locator("text=Ticket updated successfully")).to_be_visible()


class TestPaymentScenarios:
    """Test payment processing scenarios"""
    
    def test_successful_payment_flow(self, page, base_url, logged_in_customer):
        """Test successful payment processing"""
        page.goto(f"{base_url}/checkout")
        
        # Fill shipping
        page.fill('input[name="street"]', "123 Main St")
        page.fill('input[name="city"]', "New York")
        page.fill('input[name="state"]', "NY")
        page.fill('input[name="zip"]', "10001")
        page.click('button:has-text("Continue")')
        
        # Process payment
        page.frame_locator('iframe[title="Stripe"]').locator('input[name="cardnumber"]').fill("4111111111111111")
        page.frame_locator('iframe[title="Stripe"]').locator('input[name="exp-date"]').fill("12/25")
        page.frame_locator('iframe[title="Stripe"]').locator('input[name="cvc"]').fill("123")
        
        page.click('button:has-text("Pay")')
        
        # Verify success
        expect(page).to_have_url_matching(r"/order-confirmation/\d+")
    
    def test_declined_payment_flow(self, page, base_url, logged_in_customer):
        """Test declined payment handling"""
        page.goto(f"{base_url}/checkout")
        
        # Fill shipping
        page.fill('input[name="street"]', "123 Main St")
        page.fill('input[name="city"]', "New York")
        page.fill('input[name="state"]', "NY")
        page.fill('input[name="zip"]', "10001")
        page.click('button:has-text("Continue")')
        
        # Use declined test card
        page.frame_locator('iframe[title="Stripe"]').locator('input[name="cardnumber"]').fill("4000000000000002")
        page.frame_locator('iframe[title="Stripe"]').locator('input[name="exp-date"]').fill("12/25")
        page.frame_locator('iframe[title="Stripe"]').locator('input[name="cvc"]').fill("123")
        
        page.click('button:has-text("Pay")')
        
        # Verify error message
        expect(page.locator("text=Payment declined")).to_be_visible()


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_session_timeout_handling(self, page, base_url):
        """Test handling of expired session"""
        page.goto(f"{base_url}/orders")
        
        # Should redirect to login
        expect(page).to_have_url(f"{base_url}/login")
    
    def test_network_error_handling(self, page, base_url, logged_in_customer):
        """Test handling of network errors"""
        page.goto(f"{base_url}/checkout")
        
        # Simulate network error
        page.context.set_offline(True)
        page.click('button:has-text("Continue")')
        
        # Verify error message
        expect(page.locator("text=Connection error")).to_be_visible()
        
        # Restore connection
        page.context.set_offline(False)
    
    def test_form_validation_errors(self, page, base_url):
        """Test form validation error handling"""
        page.goto(f"{base_url}/register")
        
        # Submit empty form
        page.click('button:has-text("Register")')
        
        # Verify validation errors
        expect(page.locator("text=Email is required")).to_be_visible()
        expect(page.locator("text=Password is required")).to_be_visible()


class TestAccessibilityJourneys:
    """Test critical journeys for accessibility"""
    
    def test_keyboard_navigation_checkout(self, page, base_url, logged_in_customer):
        """Test keyboard navigation through checkout"""
        page.goto(f"{base_url}/checkout")
        
        # Tab through form
        page.press('input[name="street"]', 'Tab')
        page.press('input[name="city"]', 'Tab')
        page.press('input[name="state"]', 'Tab')
        
        # Fill using keyboard
        page.fill('input[name="street"]', "123 Main St")
        page.press('Tab')
        page.fill('input[name="city"]', "New York")
        
        # Submit with Enter
        page.press('button:has-text("Continue")', 'Enter')
    
    def test_screen_reader_product_details(self, page, base_url):
        """Test screen reader accessibility for product details"""
        page.goto(f"{base_url}/products/1")
        
        # Verify semantic HTML
        expect(page.locator('h1.product-title')).to_be_visible()
        expect(page.locator('p.product-description')).to_be_visible()
        
        # Verify ARIA labels
        expect(page.locator('[aria-label="Product Price"]')).to_be_visible()
        expect(page.locator('[aria-label="Add to Cart"]')).to_be_visible()
