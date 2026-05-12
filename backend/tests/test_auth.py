from http import HTTPStatus


def test_health_check(client):
    response = client.get("/api/v1/health")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"status": "ok", "service": "customer_ordering_backend"}


def test_register_and_login(client):
    payload = {
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "Str0ngPass!",
        "full_name": "Test User",
    }

    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["username"] == payload["username"]
    assert data["full_name"] == payload["full_name"]
    assert data["role"] == "customer"

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": payload["email"], "password": payload["password"]},
    )
    assert login_response.status_code == HTTPStatus.OK
    token_data = login_response.json()
    assert token_data["token_type"] == "bearer"
    assert "access_token" in token_data
