from http import HTTPStatus


def get_auth_token(client):
    register_data = {
        "email": "cartuser@example.com",
        "username": "cartuser",
        "password": "StrongCartPass1!",
        "full_name": "Cart User",
    }
    client.post("/api/v1/auth/register", json=register_data)
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": register_data["email"], "password": register_data["password"]},
    )
    assert login_response.status_code == HTTPStatus.OK
    return login_response.json()["access_token"]


def test_cart_lifecycle(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    product_payload = {
        "name": "Cart Product",
        "description": "A product for cart operations.",
        "category": "cart",
        "price": 9.99,
        "stock_quantity": 100,
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
    cart = add_response.json()
    assert cart["total"] == 19.98
    assert len(cart["items"]) == 1
    assert cart["items"][0]["quantity"] == 2

    update_response = client.put(
        f"/api/v1/cart/items/{product['id']}",
        json={"quantity": 3},
        headers=headers,
    )
    assert update_response.status_code == HTTPStatus.OK
    updated_cart = update_response.json()
    assert updated_cart["items"][0]["quantity"] == 3
    assert updated_cart["total"] == 29.97

    remove_response = client.delete(f"/api/v1/cart/items/{product['id']}", headers=headers)
    assert remove_response.status_code == HTTPStatus.OK
    removed_cart = remove_response.json()
    assert removed_cart["items"] == []
    assert removed_cart["total"] == 0.0

    clear_response = client.post("/api/v1/cart/clear", headers=headers)
    assert clear_response.status_code == HTTPStatus.OK
    cleared_cart = clear_response.json()
    assert cleared_cart["items"] == []
    assert cleared_cart["total"] == 0.0
