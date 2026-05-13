# Backend API Integration Guide

**Version**: 0.1.0  
**Base URL**: `http://localhost:8000` (development) | `https://api.example.com` (production)  
**API Documentation**: `{BASE_URL}/docs` (Swagger UI) | `{BASE_URL}/redoc` (ReDoc)

---

## Table of Contents

1. Authentication
2. Endpoints Overview
3. Request/Response Examples
4. Error Handling
5. Rate Limiting
6. WebSocket Support (Future)

---

## 1. Authentication

### JWT Token Flow

All authenticated endpoints require a JWT token in the `Authorization` header:

```http
Authorization: Bearer <access_token>
```

### Register User

```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "username": "myusername"
}
```

**Response (201 Created)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "username": "myusername",
  "role": "customer",
  "created_at": "2026-05-18T10:30:00Z"
}
```

### Login

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (200 OK)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

---

## 2. Endpoints Overview

### Health Check

```http
GET /api/v1/health
```

**Response (200 OK)**:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2026-05-18T10:30:00Z"
}
```

---

### Products

#### List Products

```http
GET /api/v1/products?page=1&limit=20&category=electronics&min_price=10&max_price=1000&sort=price
```

**Query Parameters**:
- `page` (int): Page number (default: 1)
- `limit` (int): Items per page (default: 20, max: 100)
- `category` (string): Filter by category
- `min_price` (float): Minimum price filter
- `max_price` (float): Maximum price filter
- `sort` (string): Sort by `price`, `name`, `-price`, `-name`
- `q` (string): Search query

**Response (200 OK)**:
```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "name": "Laptop Pro",
      "description": "High-performance laptop",
      "category": "electronics",
      "price": 1299.99,
      "stock_quantity": 50,
      "image_url": "https://cdn.example.com/laptop-pro.jpg",
      "created_at": "2026-05-18T10:30:00Z"
    }
  ],
  "total": 150,
  "page": 1,
  "limit": 20,
  "pages": 8
}
```

#### Get Product Details

```http
GET /api/v1/products/550e8400-e29b-41d4-a716-446655440001
```

**Response (200 OK)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "name": "Laptop Pro",
  "description": "High-performance laptop",
  "category": "electronics",
  "price": 1299.99,
  "stock_quantity": 50,
  "image_url": "https://cdn.example.com/laptop-pro.jpg",
  "rating": 4.5,
  "review_count": 125,
  "created_at": "2026-05-18T10:30:00Z"
}
```

---

### Shopping Cart

#### Get Cart

```http
GET /api/v1/cart
Authorization: Bearer <access_token>
```

**Response (200 OK)**:
```json
{
  "id": "user-cart-id",
  "items": [
    {
      "product_id": "550e8400-e29b-41d4-a716-446655440001",
      "product_name": "Laptop Pro",
      "price": 1299.99,
      "quantity": 1,
      "line_total": 1299.99
    }
  ],
  "subtotal": 1299.99,
  "tax": 103.99,
  "shipping": 10.00,
  "total": 1413.98,
  "currency": "USD"
}
```

#### Add to Cart

```http
POST /api/v1/cart/items
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "product_id": "550e8400-e29b-41d4-a716-446655440001",
  "quantity": 1
}
```

**Response (201 Created)**: Updated cart object

#### Update Cart Item

```http
PUT /api/v1/cart/items/550e8400-e29b-41d4-a716-446655440001
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "quantity": 2
}
```

#### Remove from Cart

```http
DELETE /api/v1/cart/items/550e8400-e29b-41d4-a716-446655440001
Authorization: Bearer <access_token>
```

---

### Orders

#### Create Order (Checkout)

```http
POST /api/v1/orders
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "payment_method_token": "stripe_token_xyz",
  "shipping_address": {
    "street": "123 Main St",
    "city": "Springfield",
    "state": "IL",
    "zip": "62701",
    "country": "US"
  },
  "billing_address": {
    "street": "123 Main St",
    "city": "Springfield",
    "state": "IL",
    "zip": "62701",
    "country": "US"
  }
}
```

**Response (201 Created)**:
```json
{
  "id": "order-123",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "items": [...],
  "subtotal": 1299.99,
  "tax": 103.99,
  "shipping": 10.00,
  "total_amount": 1413.98,
  "status": "processing",
  "payment_status": "paid",
  "created_at": "2026-05-18T10:30:00Z"
}
```

#### List User Orders

```http
GET /api/v1/orders?page=1&limit=10
Authorization: Bearer <access_token>
```

#### Get Order Details

```http
GET /api/v1/orders/order-123
Authorization: Bearer <access_token>
```

#### Get Order Tracking

```http
GET /api/v1/orders/order-123/tracking
Authorization: Bearer <access_token>
```

**Response (200 OK)**:
```json
{
  "order_id": "order-123",
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784",
  "carrier": "UPS",
  "tracking_url": "https://tracking.ups.com/...",
  "estimated_delivery": "2026-05-20T23:59:59Z",
  "events": [
    {
      "status": "picked_up",
      "location": "Springfield, IL",
      "timestamp": "2026-05-19T08:00:00Z"
    }
  ]
}
```

---

### Reviews

#### List Product Reviews

```http
GET /api/v1/reviews/products/550e8400-e29b-41d4-a716-446655440001?page=1&limit=10
```

**Response (200 OK)**:
```json
{
  "items": [
    {
      "id": "review-123",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "product_id": "550e8400-e29b-41d4-a716-446655440001",
      "rating": 5,
      "comment": "Excellent laptop! Very satisfied.",
      "created_at": "2026-05-18T10:30:00Z"
    }
  ],
  "total": 125,
  "average_rating": 4.5
}
```

#### Create Review

```http
POST /api/v1/reviews/products/550e8400-e29b-41d4-a716-446655440001
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "rating": 5,
  "comment": "Excellent product!"
}
```

---

### User Profile

#### Get Profile

```http
GET /api/v1/users/me
Authorization: Bearer <access_token>
```

#### Update Profile

```http
PUT /api/v1/users/me
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "username": "new_username",
  "full_name": "John Doe"
}
```

#### Change Password

```http
POST /api/v1/users/me/change-password
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "current_password": "OldPassword123!",
  "new_password": "NewPassword456!"
}
```

---

## 3. Error Handling

All errors follow a standard format:

```json
{
  "detail": "Error message description",
  "error_code": "INVALID_REQUEST",
  "status_code": 400
}
```

### Common Status Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 200 | OK | Success |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Check request parameters |
| 401 | Unauthorized | Include valid JWT token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Resource already exists or state conflict |
| 422 | Unprocessable Entity | Invalid request data |
| 429 | Too Many Requests | Rate limit exceeded, retry later |
| 500 | Server Error | Contact support |

---

## 4. Rate Limiting

Rate limits are applied per user:

- **Unauthenticated**: 100 requests per hour
- **Authenticated**: 1000 requests per hour
- **Admin**: Unlimited

Rate limit headers in response:

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1621346400
```

---

## 5. Data Types & Validation

### Common Fields

| Field | Type | Validation |
|-------|------|-----------|
| `email` | string | Valid email format |
| `password` | string | Min 8 chars, must include uppercase, lowercase, number, special char |
| `rating` | integer | 1-5 range |
| `price` | number | Positive, max 2 decimal places |
| `quantity` | integer | Positive integer |

---

## Environment Configuration

### Development

```
VITE_API_URL=http://localhost:8000
VITE_API_VERSION=v1
```

### Staging

```
VITE_API_URL=https://staging-api.example.com
VITE_API_VERSION=v1
```

### Production

```
VITE_API_URL=https://api.example.com
VITE_API_VERSION=v1
```

---

## Frontend Integration Examples

### Next API Call (TypeScript)

```typescript
import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Fetch products
const response = await apiClient.get('/api/v1/products', {
  params: {
    page: 1,
    limit: 20,
    category: 'electronics',
  },
});

console.log(response.data);
```

---

## Troubleshooting

### 401 Unauthorized

**Cause**: Missing or invalid JWT token  
**Solution**: 
1. Verify token is set in `Authorization` header
2. Check token hasn't expired
3. Log in again to get a fresh token

### 422 Unprocessable Entity

**Cause**: Invalid request body  
**Solution**: 
1. Verify all required fields are present
2. Check data types match documentation
3. Review validation rules in error details

### 429 Too Many Requests

**Cause**: Rate limit exceeded  
**Solution**: 
1. Check `X-RateLimit-Reset` header
2. Wait before making new requests
3. Implement exponential backoff in client

---

## Support

For API issues or questions:
- GitHub Issues: [project-repo/issues](https://github.com/project-repo/issues)
- Email: api-support@example.com
- Slack: #backend-support
