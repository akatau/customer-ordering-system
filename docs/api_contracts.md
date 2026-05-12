# API Contracts: Information Hiding Design

## Design Principles

API contracts are designed with information hiding as the core principle:
- **Interface Segregation**: Clients only see necessary methods and data structures
- **Implementation Hiding**: Internal business logic, database schemas, and algorithms are not exposed
- **Contract Stability**: APIs are versioned and backward-compatible
- **Error Abstraction**: Internal errors are mapped to standard HTTP codes and generic messages

## Authentication Endpoints

### POST /api/v1/auth/register
Register a new user account.

**Request Body:**
```json
{
  "email": "string (required, valid email format)",
  "password": "string (required, min 8 chars, mixed case + numbers)",
  "name": "string (required, 2-50 chars)"
}
```

**Response (201 Created):**
```json
{
  "user_id": "uuid",
  "message": "Account created successfully. Please check your email for confirmation.",
  "email_sent": true
}
```

**Error Responses:**
- 400 Bad Request: `{"error": "ValidationError", "message": "Email already exists"}`
- 500 Internal Server Error: `{"error": "ServerError", "message": "Unable to process request"}`

### POST /api/v1/auth/login
Authenticate user credentials.

**Request Body:**
```json
{
  "email": "string (required)",
  "password": "string (required)"
}
```

**Response (200 OK):**
```json
{
  "access_token": "jwt_string",
  "token_type": "Bearer",
  "expires_in": 3600,
  "user": {
    "id": "uuid",
    "email": "string",
    "name": "string"
  }
}
```

**Error Responses:**
- 401 Unauthorized: `{"error": "AuthenticationError", "message": "Invalid credentials"}`

## Product Endpoints

### GET /api/v1/products
Retrieve paginated product catalog.

**Query Parameters:**
- `page`: integer (default 1)
- `limit`: integer (default 20, max 100)
- `category`: string (optional filter)
- `search`: string (optional search term)
- `sort`: string (price_asc, price_desc, name_asc, name_desc)

**Response (200 OK):**
```json
{
  "products": [
    {
      "id": "uuid",
      "name": "string",
      "description": "string",
      "price": "number (decimal)",
      "category": "string",
      "image_url": "string",
      "in_stock": true,
      "stock_quantity": 150
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "total_pages": 8
  }
}
```

### GET /api/v1/products/{product_id}
Retrieve detailed product information.

**Response (200 OK):**
```json
{
  "id": "uuid",
  "name": "string",
  "description": "string",
  "price": "number",
  "category": "string",
  "images": ["string"],
  "specifications": {"key": "value"},
  "reviews": [
    {
      "rating": 5,
      "comment": "string",
      "user_name": "string",
      "date": "ISO8601"
    }
  ],
  "in_stock": true,
  "stock_quantity": 150
}
```

## Cart Endpoints

### GET /api/v1/cart
Retrieve current user's shopping cart.

**Response (200 OK):**
```json
{
  "items": [
    {
      "product_id": "uuid",
      "name": "string",
      "price": "number",
      "quantity": 2,
      "subtotal": "number"
    }
  ],
  "summary": {
    "subtotal": "number",
    "tax": "number",
    "shipping": "number",
    "total": "number"
  }
}
```

### POST /api/v1/cart/items
Add item to cart.

**Request Body:**
```json
{
  "product_id": "uuid",
  "quantity": 1
}
```

**Response (200 OK):**
```json
{
  "message": "Item added to cart",
  "cart_total": 2
}
```

### PUT /api/v1/cart/items/{product_id}
Update cart item quantity.

**Request Body:**
```json
{
  "quantity": 3
}
```

**Response (200 OK):**
```json
{
  "message": "Cart updated",
  "item_subtotal": "number"
}
```

## Order Endpoints

### POST /api/v1/orders
Create new order from cart.

**Request Body:**
```json
{
  "shipping_address": {
    "name": "string",
    "street": "string",
    "city": "string",
    "state": "string",
    "zip": "string",
    "country": "string"
  },
  "billing_address": {
    "same_as_shipping": true
  },
  "payment_method": {
    "type": "credit_card",
    "card_number": "string (tokenized)",
    "expiry_month": "string",
    "expiry_year": "string",
    "cvv": "string (tokenized)"
  }
}
```

**Response (201 Created):**
```json
{
  "order_id": "string",
  "status": "confirmed",
  "total": "number",
  "estimated_delivery": "ISO8601",
  "message": "Order placed successfully"
}
```

### GET /api/v1/orders/{order_id}
Retrieve order details.

**Response (200 OK):**
```json
{
  "id": "string",
  "status": "processing|shipped|delivered",
  "items": [
    {
      "product_id": "uuid",
      "name": "string",
      "quantity": 2,
      "price": "number"
    }
  ],
  "shipping_address": {...},
  "tracking_number": "string",
  "created_at": "ISO8601",
  "updated_at": "ISO8601"
}
```

## Administrative Endpoints

### POST /api/v1/admin/products
Create new product (Admin only).

**Request Body:**
```json
{
  "name": "string",
  "description": "string",
  "price": "number",
  "category": "string",
  "stock_quantity": 100
}
```

**Response (201 Created):**
```json
{
  "product_id": "uuid",
  "message": "Product created"
}
```

### POST /api/v1/admin/invoices/{order_id}
Generate invoice for order (Admin/Support only).

**Response (200 OK):**
```json
{
  "invoice_url": "string",
  "message": "Invoice generated and emailed"
}
```

## Password Recovery Endpoints

### POST /api/v1/auth/forgot-password
Initiate password reset.

**Request Body:**
```json
{
  "email": "string (required)"
}
```

**Response (200 OK):**
```json
{
  "message": "If an account with that email exists, a reset link has been sent."
}
```

### POST /api/v1/auth/reset-password
Reset password with token.

**Request Body:**
```json
{
  "token": "string (from email)",
  "password": "string (new password)"
}
```

**Response (200 OK):**
```json
{
  "message": "Password reset successfully"
}
```

## Review Endpoints

### GET /api/v1/products/{product_id}/reviews
Get product reviews.

**Query Parameters:**
- `page`: integer (default 1)
- `limit`: integer (default 10)

**Response (200 OK):**
```json
{
  "reviews": [
    {
      "id": "uuid",
      "rating": 5,
      "comment": "string",
      "user_name": "string",
      "created_at": "ISO8601",
      "can_edit": true
    }
  ],
  "pagination": {...}
}
```

### POST /api/v1/products/{product_id}/reviews
Submit product review.

**Request Body:**
```json
{
  "rating": 5,
  "comment": "string (max 500 chars)"
}
```

**Response (201 Created):**
```json
{
  "review_id": "uuid",
  "message": "Review submitted"
}
```

### PUT /api/v1/reviews/{review_id}
Update own review.

**Request Body:**
```json
{
  "rating": 4,
  "comment": "Updated comment"
}
```

**Response (200 OK):**
```json
{
  "message": "Review updated"
}
```

## Discount Endpoints

### POST /api/v1/cart/discount
Apply discount code to cart.

**Request Body:**
```json
{
  "code": "string"
}
```

**Response (200 OK):**
```json
{
  "discount_amount": "number",
  "new_total": "number",
  "message": "Discount applied"
}
```

## Payment Method Endpoints

### GET /api/v1/payment-methods
Get user's saved payment methods.

**Response (200 OK):**
```json
{
  "methods": [
    {
      "id": "uuid",
      "type": "credit_card",
      "last4": "4242",
      "brand": "visa",
      "expiry_month": 12,
      "expiry_year": 2025
    }
  ]
}
```

### POST /api/v1/payment-methods
Save payment method.

**Request Body:**
```json
{
  "type": "credit_card",
  "card_token": "string (from frontend tokenization)",
  "expiry_month": 12,
  "expiry_year": 2025
}
```

**Response (201 Created):**
```json
{
  "method_id": "uuid",
  "message": "Payment method saved"
}
```

### DELETE /api/v1/payment-methods/{method_id}
Delete saved payment method.

**Response (200 OK):**
```json
{
  "message": "Payment method deleted"
}
```

## Administrative Endpoints

### GET /api/v1/admin/user-activity
Get user activity logs (Admin only).

**Query Parameters:**
- `user_id`: uuid (optional)
- `action`: string (optional)
- `start_date`: ISO8601 (optional)
- `end_date`: ISO8601 (optional)

**Response (200 OK):**
```json
{
  "logs": [
    {
      "id": "uuid",
      "user_id": "uuid",
      "action": "login",
      "timestamp": "ISO8601",
      "ip_address": "string",
      "details": {}
    }
  ]
}
```

## Support Endpoints

### POST /api/v1/support/tickets
Create support ticket.

**Request Body:**
```json
{
  "subject": "string",
  "category": "order_issue|product_question|refund",
  "priority": "low|medium|high",
  "description": "string"
}
```

**Response (201 Created):**
```json
{
  "ticket_id": "uuid",
  "message": "Ticket created"
}
```

### GET /api/v1/support/tickets
Get support tickets (Support only).

**Response (200 OK):**
```json
{
  "tickets": [
    {
      "id": "uuid",
      "subject": "string",
      "status": "open|in_progress|resolved",
      "priority": "low|medium|high",
      "created_at": "ISO8601",
      "customer_email": "string"
    }
  ]
}
```

### PUT /api/v1/support/tickets/{ticket_id}
Update ticket status (Support only).

**Request Body:**
```json
{
  "status": "resolved",
  "notes": "string"
}
```

**Response (200 OK):**
```json
{
  "message": "Ticket updated"
}
```

## Security & Headers

All endpoints require:
- `Authorization: Bearer {token}` for authenticated requests
- `Content-Type: application/json`
- `X-API-Version: v1`

Rate limiting: 100 requests per minute per IP.

CORS enabled for frontend domains.

## Implementation Hiding

- Database models/schemas not exposed in API
- Business logic encapsulated in service layers
- External service integrations abstracted
- Error details sanitized for security
- Response formats stable across internal changes

This contract allows frontend teams and external consumers to integrate without knowledge of internal Python implementation details.
