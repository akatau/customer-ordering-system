from http import HTTPStatus


def get_auth_token(client):
    register_data = {
        "email": "orderuser@example.com",
        "username": "orderuser",
        "password": "StrongOrderPass1!",
        "full_name": "Order User",
    }
    client.post("/api/v1/auth/register", json=register_data)
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": register_data["email"], "password": register_data["password"]},
    )
    assert login_response.status_code == HTTPStatus.OK
    return login_response.json()["access_token"]


def test_order_checkout_flow(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    product_payload = {
        "name": "Checkout Product",
        "description": "A product for checkout tests.",
        "category": "checkout",
        "price": 15.00,
        "stock_quantity": 10,
    }
    product_response = client.post("/api/v1/products/", json=product_payload)
    assert product_response.status_code == HTTPStatus.CREATED
    product = product_response.json()

    add_response = client.post(
        "/api/v1/cart/items",
        json={"product_id": product["id"], "quantity": 2},
        headers=headers,
    )
    assert add_response.status_code == HTTPStatus.CREATED

    order_payload = {
        "shipping_address": "123 Test Lane, Test City, TC 12345",
        "billing_address": "123 Test Lane, Test City, TC 12345",
        "payment_method": "test_card_success",
        "items": [{"product_id": product["id"], "quantity": 2}],
    }
    create_response = client.post("/api/v1/orders/", json=order_payload, headers=headers)
    assert create_response.status_code == HTTPStatus.CREATED
    order = create_response.json()
    assert order["status"] in ["processing", "completed"]
    assert order["total_amount"] == "30.00"
    assert len(order["items"]) == 1
    assert order["items"][0]["quantity"] == 2

    list_response = client.get("/api/v1/orders/", headers=headers)
    assert list_response.status_code == HTTPStatus.OK
    assert any(o["id"] == order["id"] for o in list_response.json())

    detail_response = client.get(f"/api/v1/orders/{order['id']}", headers=headers)
    assert detail_response.status_code == HTTPStatus.OK
    detail = detail_response.json()
    assert detail["id"] == order["id"]
    assert detail["user_id"] == order["user_id"]
