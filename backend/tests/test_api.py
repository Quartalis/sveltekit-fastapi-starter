"""API tests: health, registration, login, and the protected /api/me route."""

from datetime import timedelta

from jose import jwt

import main
from config import settings


# --- /api/health ---

def test_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "version": "1.0.0", "edition": "free"}


# --- /api/auth/register ---

def test_register_returns_user_without_password(client, user):
    resp = client.post("/api/auth/register", json=user)
    assert resp.status_code == 200
    body = resp.json()
    assert body["email"] == user["email"]
    assert body["name"] == user["name"]
    assert "created_at" in body
    assert "password" not in body and "hashed_password" not in body


def test_register_stores_hashed_password_not_plaintext(client, user):
    client.post("/api/auth/register", json=user)
    stored = main.fake_users_db[user["email"]]
    assert stored["hashed_password"] != user["password"]
    assert main.verify_password(user["password"], stored["hashed_password"])


def test_register_duplicate_email_is_rejected(client, registered_user):
    resp = client.post("/api/auth/register", json=registered_user)
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Email already registered"


def test_register_invalid_email_is_rejected(client, user):
    resp = client.post("/api/auth/register", json={**user, "email": "not-an-email"})
    assert resp.status_code == 422


def test_register_missing_field_is_rejected(client):
    resp = client.post("/api/auth/register", json={"email": "bob@example.com"})
    assert resp.status_code == 422


# --- /api/auth/login ---

def test_login_returns_bearer_token(client, registered_user):
    resp = client.post(
        "/api/auth/login",
        data={"username": registered_user["email"], "password": registered_user["password"]},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["token_type"] == "bearer"
    payload = jwt.decode(body["access_token"], settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    assert payload["sub"] == registered_user["email"]
    assert "exp" in payload


def test_login_wrong_password(client, registered_user):
    resp = client.post(
        "/api/auth/login",
        data={"username": registered_user["email"], "password": "wrong"},
    )
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Invalid credentials"


def test_login_unknown_user(client):
    resp = client.post("/api/auth/login", data={"username": "nobody@example.com", "password": "x"})
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Invalid credentials"


# --- /api/me ---

def test_me_with_valid_token(client, registered_user, auth_headers):
    resp = client.get("/api/me", headers=auth_headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["email"] == registered_user["email"]
    assert body["name"] == registered_user["name"]


def test_me_without_token(client):
    resp = client.get("/api/me")
    assert resp.status_code == 401
    assert resp.headers.get("www-authenticate", "").lower().startswith("bearer")


def test_me_with_garbage_token(client):
    resp = client.get("/api/me", headers={"Authorization": "Bearer not.a.jwt"})
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Invalid or expired token"


def test_me_with_token_signed_by_wrong_secret(client, registered_user):
    forged = jwt.encode({"sub": registered_user["email"]}, "someone-elses-secret", algorithm=settings.JWT_ALGORITHM)
    resp = client.get("/api/me", headers={"Authorization": f"Bearer {forged}"})
    assert resp.status_code == 401


def test_me_with_expired_token(client, registered_user):
    expired = main.create_access_token({"sub": registered_user["email"]}, expires_delta=timedelta(seconds=-1))
    resp = client.get("/api/me", headers={"Authorization": f"Bearer {expired}"})
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Invalid or expired token"


def test_me_with_token_for_deleted_user(client, registered_user, auth_headers):
    # A valid token whose subject no longer exists must not be accepted.
    main.fake_users_db.clear()
    resp = client.get("/api/me", headers=auth_headers)
    assert resp.status_code == 401
