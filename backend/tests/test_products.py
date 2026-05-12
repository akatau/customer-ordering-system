from http import HTTPStatus


def test_list_and_create_product(client):
    product_payload = {
        "name": "Test Product",
        "description": "A product used for unit testing.",
        "category": "testing",
        "price": 19.99,
        "stock_quantity": 50,
    }

    create_response = client.post("/api/v1/products/", json=product_payload)
    assert create_response.status_code == HTTPStatus.CREATED
    created = create_response.json()
    assert created["name"] == product_payload["name"]
    assert created["category"] == product_payload["category"]
    assert created["stock_quantity"] == product_payload["stock_quantity"]

    list_response = client.get("/api/v1/products/?page=1&limit=10")
    assert list_response.status_code == HTTPStatus.OK
    data = list_response.json()
    assert data["total"] >= 1
    assert any(item["id"] == created["id"] for item in data["data"])

    detail_response = client.get(f"/api/v1/products/{created['id']}")
    assert detail_response.status_code == HTTPStatus.OK
    detail = detail_response.json()
    assert detail["name"] == product_payload["name"]
