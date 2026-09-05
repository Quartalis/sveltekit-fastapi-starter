"""Shared fixtures for the backend test suite."""

import os
import sys

import pytest
from fastapi.testclient import TestClient

# main.py uses flat imports (`from config import settings`), so put backend/ on the path.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import main  # noqa: E402


@pytest.fixture(autouse=True)
def clean_user_store():
    """Every test starts with an empty user store."""
    main.fake_users_db.clear()
    yield
    main.fake_users_db.clear()


@pytest.fixture
def client():
    with TestClient(main.app) as c:
        yield c


@pytest.fixture
def user():
    return {"email": "alice@example.com", "password": "correct horse battery", "name": "Alice"}


@pytest.fixture
def registered_user(client, user):
    resp = client.post("/api/auth/register", json=user)
    assert resp.status_code == 200, resp.text
    return user


@pytest.fixture
def auth_headers(client, registered_user):
    resp = client.post(
        "/api/auth/login",
        data={"username": registered_user["email"], "password": registered_user["password"]},
    )
    assert resp.status_code == 200, resp.text
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}
