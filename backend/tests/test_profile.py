from http import HTTPStatus


def get_auth_token(client):
    register_data = {
        "email": "profileuser@example.com",
        "username": "profileuser",
        "password": "StrongProfile1!",
        "full_name": "Profile User",
    }
    client.post("/api/v1/auth/register", json=register_data)
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": register_data["email"], "password": register_data["password"]},
    )
    assert login_response.status_code == HTTPStatus.OK
    return login_response.json()["access_token"]


def test_profile_read_and_update(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    profile_response = client.get("/api/v1/users/me", headers=headers)
    assert profile_response.status_code == HTTPStatus.OK
    profile = profile_response.json()
    assert profile["username"] == "profileuser"

    update_payload = {"full_name": "Updated Profile User", "username": "updatedprofileuser"}
    update_response = client.put("/api/v1/users/me", json=update_payload, headers=headers)
    assert update_response.status_code == HTTPStatus.OK
    updated = update_response.json()
    assert updated["full_name"] == "Updated Profile User"
    assert updated["username"] == "updatedprofileuser"


def test_change_password(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    change_response = client.post(
        "/api/v1/users/me/change-password",
        json={"current_password": "StrongProfile1!", "new_password": "NewStrongProfile2!"},
        headers=headers,
    )
    assert change_response.status_code == HTTPStatus.NO_CONTENT

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "profileuser@example.com", "password": "NewStrongProfile2!"},
    )
    assert login_response.status_code == HTTPStatus.OK
