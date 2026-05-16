/**
 * QA Sprint Week 7: E2E Critical User Journey Tests
 * Tests for critical user workflows and integration
 */
import { test, expect } from '@playwright/test';

test.describe('Customer Journeys', () => {
    
    test('User Registration → Login → Browse Products', async ({ page, baseURL }) => {
        // Register new user
        await page.goto(`${baseURL}/register`);
        await page.fill('input[name="email"]', 'testuser@example.com');
        await page.fill('input[name="password"]', 'SecurePassword123!');
        await page.fill('input[name="firstName"]', 'Test');
        await page.fill('input[name="lastName"]', 'User');
        await page.click('button:has-text("Register")');
        
        // Verify registration success
        await expect(page).toHaveURL(`${baseURL}/login`);
        
        // Login
        await page.fill('input[name="email"]', 'testuser@example.com');
        await page.fill('input[name="password"]', 'SecurePassword123!');
        await page.click('button:has-text("Login")');
        
        // Verify logged in
        await expect(page).toHaveURL(`${baseURL}/home`);
        await expect(page.locator('text=Welcome, Test')).toBeVisible();
        
        // Browse products
        await page.click('a:has-text("Products")');
        await expect(page).toHaveURL(`${baseURL}/products`);
        
        // Verify products loaded
        const productsCount = await page.locator('.product-item').count();
        expect(productsCount).toBeGreaterThan(0);
    });

    test('Product Search → Filter → View Details', async ({ page, baseURL }) => {
        await page.goto(`${baseURL}/products`);
        
        // Search for products
        await page.fill('input[placeholder="Search products..."]', 'laptop');
        await page.click('button:has-text("Search")');
        
        // Filter by price
        await page.click('text=Filter');
        await page.fill('input[name="minPrice"]', '500');
        await page.fill('input[name="maxPrice"]', '1500');
        await page.click('button:has-text("Apply Filters")');
        
        // Verify filtered results
        const products = await page.locator('.product-item').all();
        for (const product of products) {
            const priceText = await product.locator('.product-price').textContent();
            const price = parseFloat(priceText?.replace('$', '') || '0');
            expect(price).toBeGreaterThanOrEqual(500);
            expect(price).toBeLessThanOrEqual(1500);
        }
        
        // Click on first product
        await page.locator('.product-item').first().click();
        
        // Verify product details
        await expect(page).toHaveURL(/\/products\/\d+/);
        await expect(page.locator('.product-title')).toBeVisible();
        await expect(page.locator('.product-description')).toBeVisible();
    });

    test('Add to Cart → Checkout → Payment', async ({ page, baseURL }) => {
        // Note: Assuming auth state is handled via Playwright fixtures/storageState beforehand
        await page.goto(`${baseURL}/products`);
        
        // Add product to cart
        await page.locator('.product-item').first().click();
        await page.fill('input[name="quantity"]', '2');
        await page.click('button:has-text("Add to Cart")');
        
        // Verify cart updated
        await expect(page.locator('.cart-badge')).toContainText('2');
        
        // Go to cart
        await page.click('a:has-text("Cart")');
        await expect(page).toHaveURL(`${baseURL}/cart`);
        
        // Verify items in cart
        await expect(page.locator('.cart-item')).toHaveCount(1);
        
        // Proceed to checkout
        await page.click('button:has-text("Checkout")');
        await expect(page).toHaveURL(`${baseURL}/checkout`);
        
        // Fill shipping address
        await page.fill('input[name="street"]', '123 Main St');
        await page.fill('input[name="city"]', 'New York');
        await page.fill('input[name="state"]', 'NY');
        await page.fill('input[name="zip"]', '10001');
        await page.click('button:has-text("Continue to Payment")');
        
        // Fill payment information
        const stripeFrame = page.frameLocator('iframe[title="Stripe"]');
        await stripeFrame.locator('input[name="cardnumber"]').fill('4111111111111111');
        await stripeFrame.locator('input[name="exp-date"]').fill('12/25');
        await stripeFrame.locator('input[name="cvc"]').fill('123');
        
        // Place order
        await page.click('button:has-text("Place Order")');
        
        // Verify order confirmation
        await expect(page).toHaveURL(/\/order-confirmation\/\d+/);
        await expect(page.locator('text=Order Confirmed')).toBeVisible();
    });

    test('Order Confirmation → Tracking', async ({ page, baseURL }) => {
        // Navigate to orders
        await page.goto(`${baseURL}/orders`);
        
        // Click on first order
        await page.locator('.order-item').first().click();
        
        // Verify order details
        await expect(page).toHaveURL(/\/orders\/\d+/);
        await expect(page.locator('.order-status')).toBeVisible();
        
        // Verify tracking information
        const trackingNumber = await page.locator('.tracking-number').textContent();
        expect(trackingNumber).toBeTruthy();
        
        // Click track shipment
        await page.click('button:has-text("Track Shipment")');
        
        // Verify tracking page
        await expect(page).toHaveURL(/\/track\//);
        await expect(page.locator('.tracking-timeline')).toBeVisible();
    });
});

test.describe('Admin Journeys', () => {
    
    test('Admin Product Management', async ({ page, baseURL }) => {
        await page.goto(`${baseURL}/admin/products`);
        await expect(page).toHaveURL(`${baseURL}/admin/products`);
        
        // Add new product
        await page.click('button:has-text("Add Product")');
        await expect(page).toHaveURL(`${baseURL}/admin/products/new`);
        
        // Fill product form
        await page.fill('input[name="name"]', 'New Product');
        await page.fill('textarea[name="description"]', 'Test product description');
        await page.fill('input[name="price"]', '99.99');
        await page.fill('input[name="stock"]', '100');
        await page.selectOption('select[name="category"]', 'Electronics');
        await page.click('button:has-text("Save Product")');
        
        // Verify product created
        await expect(page).toHaveURL(`${baseURL}/admin/products`);
        await expect(page.locator('text=Product created successfully')).toBeVisible();
        
        // Verify new product in list
        await expect(page.locator('text=New Product')).toBeVisible();
    });

    test('Admin Order Management', async ({ page, baseURL }) => {
        await page.goto(`${baseURL}/admin/orders`);
        
        // Click on first order
        await page.locator('.order-item').first().click();
        
        // Update order status
        await page.selectOption('select[name="status"]', 'shipped');
        await page.click('button:has-text("Update Status")');
        
        // Verify status updated
        await expect(page.locator('text=Order updated successfully')).toBeVisible();
        await expect(page.locator('.order-status')).toContainText('Shipped');
    });

    test('Admin User Management', async ({ page, baseURL }) => {
        await page.goto(`${baseURL}/admin/users`);
        
        // Search for user
        await page.fill('input[placeholder="Search users..."]', 'test@example.com');
        await page.click('button:has-text("Search")');
        
        // Verify user found
        const userCount = await page.locator('.user-item').count();
        expect(userCount).toBeGreaterThan(0);
        
        // Click on user
        await page.locator('.user-item').first().click();
        
        // View user details
        await expect(page).toHaveURL(/\/admin\/users\/\d+/);
        await expect(page.locator('.user-email')).toBeVisible();
    });
});

test.describe('Support Journeys', () => {
    
    test('Support Ticket Creation', async ({ page, baseURL }) => {
        await page.goto(`${baseURL}/support/tickets`);
        
        // Create new ticket
        await page.click('button:has-text("Create Ticket")');
        
        // Fill ticket form
        await page.fill('input[name="subject"]', 'Product Defect');
        await page.selectOption('select[name="category"]', 'Product Quality');
        await page.fill('textarea[name="description"]', 'The product arrived with defects');
        await page.click('button:has-text("Submit")');
        
        // Verify ticket created
        await expect(page).toHaveURL(/\/support\/tickets\/\d+/);
        await expect(page.locator('text=Ticket created successfully')).toBeVisible();
    });

    test('Support Ticket Resolution', async ({ page, baseURL }) => {
        await page.goto(`${baseURL}/admin/support/tickets`);
        
        // Filter open tickets
        await page.selectOption('select[name="status"]', 'open');
        await page.click('button:has-text("Filter")');
        
        // Click on first ticket
        await page.locator('.ticket-item').first().click();
        
        // Add response
        await page.fill('textarea[name="response"]', 'We will send a replacement');
        await page.click('button:has-text("Send Response")');
        
        // Update ticket status
        await page.selectOption('select[name="status"]', 'resolved');
        await page.click('button:has-text("Update")');
        
        // Verify ticket resolved
        await expect(page.locator('text=Ticket updated successfully')).toBeVisible();
    });
});

test.describe('Payment Scenarios', () => {
    
    test('Successful Payment Flow', async ({ page, baseURL }) => {
        await page.goto(`${baseURL}/checkout`);
        
        // Fill shipping
        await page.fill('input[name="street"]', '123 Main St');
        await page.fill('input[name="city"]', 'New York');
        await page.fill('input[name="state"]', 'NY');
        await page.fill('input[name="zip"]', '10001');
        await page.click('button:has-text("Continue")');
        
        // Process payment
        const stripeFrame = page.frameLocator('iframe[title="Stripe"]');
        await stripeFrame.locator('input[name="cardnumber"]').fill('4111111111111111');
        await stripeFrame.locator('input[name="exp-date"]').fill('12/25');
        await stripeFrame.locator('input[name="cvc"]').fill('123');
        
        await page.click('button:has-text("Pay")');
        
        // Verify success
        await expect(page).toHaveURL(/\/order-confirmation\/\d+/);
    });

    test('Declined Payment Flow', async ({ page, baseURL }) => {
        await page.goto(`${baseURL}/checkout`);
        
        // Fill shipping
        await page.fill('input[name="street"]', '123 Main St');
        await page.fill('input[name="city"]', 'New York');
        await page.fill('input[name="state"]', 'NY');
        await page.fill('input[name="zip"]', '10001');
        await page.click('button:has-text("Continue")');
        
        // Use declined test card
        const stripeFrame = page.frameLocator('iframe[title="Stripe"]');
        await stripeFrame.locator('input[name="cardnumber"]').fill('4000000000000002');
        await stripeFrame.locator('input[name="exp-date"]').fill('12/25');
        await stripeFrame.locator('input[name="cvc"]').fill('123');
        
        await page.click('button:has-text("Pay")');
        
        // Verify error message
        await expect(page.locator('text=Payment declined')).toBeVisible();
    });
});

test.describe('Error Handling', () => {
    
    test('Session Timeout Handling', async ({ page, baseURL }) => {
        await page.goto(`${baseURL}/orders`);
        // Should redirect to login
        await expect(page).toHaveURL(`${baseURL}/login`);
    });

    test('Network Error Handling', async ({ page, baseURL, context }) => {
        await page.goto(`${baseURL}/checkout`);
        
        // Simulate network error
        await context.setOffline(true);
        await page.click('button:has-text("Continue")');
        
        // Verify error message
        await expect(page.locator('text=Connection error')).toBeVisible();
        
        // Restore connection
        await context.setOffline(false);
    });

    test('Form Validation Errors', async ({ page, baseURL }) => {
        await page.goto(`${baseURL}/register`);
        
        // Submit empty form
        await page.click('button:has-text("Register")');
        
        // Verify validation errors
        await expect(page.locator('text=Email is required')).toBeVisible();
        await expect(page.locator('text=Password is required')).toBeVisible();
    });
});

test.describe('Accessibility Journeys', () => {
    
    test('Keyboard Navigation Checkout', async ({ page, baseURL }) => {
        await page.goto(`${baseURL}/checkout`);
        
        // Tab through form
        await page.locator('input[name="street"]').press('Tab');
        await page.locator('input[name="city"]').press('Tab');
        await page.locator('input[name="state"]').press('Tab');
        
        // Fill using keyboard
        await page.fill('input[name="street"]', '123 Main St');
        await page.keyboard.press('Tab');
        await page.fill('input[name="city"]', 'New York');
        
        // Submit with Enter
        await page.locator('button:has-text("Continue")').press('Enter');
    });

    test('Screen Reader Product Details', async ({ page, baseURL }) => {
        await page.goto(`${baseURL}/products/1`);
        
        // Verify semantic HTML
        await expect(page.locator('h1.product-title')).toBeVisible();
        await expect(page.locator('p.product-description')).toBeVisible();
        
        // Verify ARIA labels
        await expect(page.locator('[aria-label="Product Price"]')).toBeVisible();
        await expect(page.locator('[aria-label="Add to Cart"]')).toBeVisible();
    });
});
