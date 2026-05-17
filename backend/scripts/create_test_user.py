import requests

base = "http://127.0.0.1:8000/api/v1"
payload = {
    "email": "localtester@example.com",
    "username": "localtester",
    "password": "TestPass123!",
    "full_name": "Local Tester"
}

r = requests.post(f"{base}/auth/register", json=payload)
print("register", r.status_code, r.text)
if r.status_code == 201:
    t = requests.post(f"{base}/auth/login", json={"email": payload["email"], "password": payload["password"]})
    print("login", t.status_code, t.text)
else:
    print("skipping login")
