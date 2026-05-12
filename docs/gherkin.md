# Gherkin Scenarios

Structured Gherkin syntax scenarios for core user stories, following BDD principles.

## Customer Registration (US-001)

**Scenario: Successful user registration**  
Given I am on the registration page  
And I have not previously registered with this email  
When I enter valid registration details (name, unique email, secure password)  
And I submit the registration form  
Then I should be redirected to the login page  
And I should receive a confirmation email  
And my account should be created in the system  

**Scenario: Registration with existing email**  
Given I am on the registration page  
And an account already exists with the email "existing@example.com"  
When I enter registration details with email "existing@example.com"  
And I submit the registration form  
Then I should see an error message "Email already registered"  
And I should remain on the registration page  
And no new account should be created  

**Scenario: Registration with weak password**  
Given I am on the registration page  
When I enter registration details with password "123"  
And I submit the registration form  
Then I should see an error message about password requirements  
And I should remain on the registration page  

## User Login (US-002)

**Scenario: Successful login**  
Given I am on the login page  
And I have a registered account with email "user@example.com" and password "ValidPass123"  
When I enter email "user@example.com" and password "ValidPass123"  
And I submit the login form  
Then I should be redirected to the product catalog  
And I should be authenticated for the session  

**Scenario: Invalid credentials**  
Given I am on the login page  
When I enter email "user@example.com" and password "WrongPass123"  
And I submit the login form  
Then I should see an error message "Invalid credentials"  
And I should remain on the login page  

## Browse Products (US-003)

**Scenario: View product catalog**  
Given I am on the product catalog page  
And products exist in the system  
When I view the page  
Then I should see a grid of products  
And each product should display image, name, price, and availability status  
And I should see pagination controls if there are more than 20 products  

**Scenario: Filter products by category**  
Given I am on the product catalog page  
And products exist in multiple categories  
When I select category "Electronics" from the filter  
Then I should see only products in the "Electronics" category  
And the filter should remain applied  

## Add to Cart (US-006)

**Scenario: Add product to cart**  
Given I am viewing a product details page  
And the product is in stock  
When I click "Add to Cart"  
And I specify quantity "2"  
Then the product should be added to my cart  
And I should see a confirmation message  
And the cart icon should show updated item count  

**Scenario: Add out-of-stock product**  
Given I am viewing a product details page  
And the product is out of stock  
When I click "Add to Cart"  
Then I should see an error message "Product out of stock"  
And the product should not be added to cart  

## Checkout Process (US-007)

**Scenario: Complete checkout**  
Given I have items in my cart  
And I am logged in  
And I am on the checkout page  
When I enter valid shipping and billing information  
And I enter valid payment details  
And I submit the order  
Then I should see an order confirmation page  
And I should receive an order confirmation email  
And my cart should be emptied  
And an order record should be created  

**Scenario: Checkout with invalid payment**  
Given I have items in my cart  
And I am on the checkout page  
When I enter invalid payment details  
And I submit the order  
Then I should see an error message "Payment failed"  
And I should remain on the checkout page  
And no order should be created  

## Order Tracking (US-008)

**Scenario: View order status**  
Given I have placed an order with ID "ORD-12345"  
And I am logged in  
And I am on my order history page  
When I view order "ORD-12345"  
Then I should see the current status (e.g., "Processing")  
And I should see estimated delivery date  
And I should see order details (items, quantities, totals)  

**Scenario: Track shipped order**  
Given I have a shipped order with tracking number "TRACK-67890"  
And I am viewing the order details  
When I click on the tracking number  
Then I should be redirected to the shipping provider's tracking page  

## Password Recovery (US-015)

**Scenario: Successful password reset**  
Given I am on the login page  
And I have forgotten my password  
When I click "Forgot Password"  
And I enter my email "user@example.com"  
And I submit the reset request  
Then I should see a confirmation message  
And I should receive an email with reset link  
And the link should be valid for 1 hour  

**Scenario: Reset password with valid link**  
Given I have received a password reset email  
And the link is still valid  
When I click the reset link  
And I enter a new password "NewSecure123"  
And I confirm the new password  
Then my password should be updated  
And I should be redirected to login  
And I should be able to login with the new password  

## Product Reviews (US-016)

**Scenario: View product reviews**  
Given I am viewing a product details page  
And the product has reviews  
When I scroll to the reviews section  
Then I should see a list of reviews with ratings and comments  
And I should see pagination if there are more than 10 reviews  

**Scenario: Submit product review**  
Given I have purchased a product  
And I am logged in  
And I am viewing the product details  
When I click "Write Review"  
And I enter rating "5" and comment "Great product!"  
And I submit the review  
Then the review should be added to the product  
And I should see a confirmation message  

## Apply Discounts (US-017)

**Scenario: Apply valid discount code**  
Given I have items in my cart  
And I have a valid discount code "SAVE10"  
When I enter the code in the discount field  
And I apply the discount  
Then the discount should be applied to my cart  
And the total should be reduced by 10%  
And I should see the discount amount  

**Scenario: Apply invalid discount code**  
Given I have items in my cart  
When I enter an invalid code "INVALID"  
And I apply the discount  
Then I should see an error message "Invalid discount code"  
And the cart total should remain unchanged  

These Gherkin scenarios provide executable specifications for automated testing and ensure clear understanding of expected system behavior.
