from http import HTTPStatus


def get_auth_token(client):
    register_data = {
        "email": "reviewer@example.com",
        "username": "reviewer",
        "password": "StrongReview1!",
        "full_name": "Reviewer",
    }
    client.post("/api/v1/auth/register", json=register_data)
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": register_data["email"], "password": register_data["password"]},
    )
    assert login_response.status_code == HTTPStatus.OK
    return login_response.json()["access_token"]


def test_review_lifecycle(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    product_payload = {
        "name": "Review Product",
        "description": "A product for review tests.",
        "category": "reviews",
        "price": 20.00,
        "stock_quantity": 10,
    }
    product_response = client.post("/api/v1/products/", json=product_payload)
    assert product_response.status_code == HTTPStatus.CREATED
    product = product_response.json()

    order_payload = {
        "shipping_address": "123 Review Lane",
        "billing_address": "123 Review Lane",
        "payment_method": "test_card_success",
        "items": [{"product_id": product["id"], "quantity": 1}],
    }
    create_order = client.post("/api/v1/orders/", json=order_payload, headers=headers)
    assert create_order.status_code == HTTPStatus.CREATED

    review_payload = {"rating": 5, "comment": "Excellent product"}
    create_response = client.post(f"/api/v1/reviews/products/{product['id']}", json=review_payload, headers=headers)
    assert create_response.status_code == HTTPStatus.CREATED
    review = create_response.json()
    assert review["rating"] == 5
    assert review["comment"] == "Excellent product"

    list_response = client.get(f"/api/v1/reviews/products/{product['id']}")
    assert list_response.status_code == HTTPStatus.OK
    reviews = list_response.json()
    assert any(r["id"] == review["id"] for r in reviews)

    update_response = client.put(
        f"/api/v1/reviews/{review['id']}",
        json={"rating": 4, "comment": "Great product"},
        headers=headers,
    )
    assert update_response.status_code == HTTPStatus.OK
    updated = update_response.json()
    assert updated["rating"] == 4
    assert updated["comment"] == "Great product"

    delete_response = client.delete(f"/api/v1/reviews/{review['id']}", headers=headers)
    assert delete_response.status_code == HTTPStatus.NO_CONTENT
