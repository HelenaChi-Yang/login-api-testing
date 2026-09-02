import os
from datetime import UTC, datetime, timedelta

os.environ["JWT_SIGNING_KEY"] = "test-signing-key"

import jwt
import pytest
from fastapi.testclient import TestClient

from src.login_api.main import (
    FAILED_LOGIN_ATTEMPTS,
    LOCKOUT_FAILED_ATTEMPT_LIMIT,
    TOKEN_ALGORITHM,
    TOKEN_SIGNING_KEY,
    VALID_ACCOUNT,
    VALID_PASSWORD,
    app,
)

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_login_attempts() -> None:
    FAILED_LOGIN_ATTEMPTS.clear()
    yield
    FAILED_LOGIN_ATTEMPTS.clear()


def login_successfully() -> str:
    response = client.post(
        "/login",
        json={"account": VALID_ACCOUNT, "password": VALID_PASSWORD},
    )

    return response.json()["access_token"]


def test_health_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root_returns_login_page() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "Login Page" in response.text
    assert 'id="login-form"' in response.text


def test_login_with_valid_credentials_returns_access_token() -> None:
    response = client.post(
        "/login",
        json={"account": VALID_ACCOUNT, "password": VALID_PASSWORD},
    )

    body = response.json()

    assert response.status_code == 200
    assert body["message"] == "Login successful"
    assert body["account"] == VALID_ACCOUNT
    assert body["token_type"] == "Bearer"
    assert body["access_token"] != ""


def test_login_with_invalid_credentials_returns_401() -> None:
    response = client.post(
        "/login",
        json={"account": VALID_ACCOUNT, "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid account or password"}


def test_login_locks_account_after_three_failed_password_attempts() -> None:
    for _ in range(LOCKOUT_FAILED_ATTEMPT_LIMIT):
        response = client.post(
            "/login",
            json={"account": VALID_ACCOUNT, "password": "wrong-password"},
        )

        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid account or password"}

    response = client.post(
        "/login",
        json={"account": VALID_ACCOUNT, "password": VALID_PASSWORD},
    )

    assert response.status_code == 423
    assert response.json() == {"detail": "Account locked"}


def test_successful_login_before_lockout_resets_failed_attempts() -> None:
    for _ in range(LOCKOUT_FAILED_ATTEMPT_LIMIT - 1):
        response = client.post(
            "/login",
            json={"account": VALID_ACCOUNT, "password": "wrong-password"},
        )

        assert response.status_code == 401

    login_response = client.post(
        "/login",
        json={"account": VALID_ACCOUNT, "password": VALID_PASSWORD},
    )

    assert login_response.status_code == 200

    response = client.post(
        "/login",
        json={"account": VALID_ACCOUNT, "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid account or password"}


def test_invalid_account_attempts_do_not_lock_valid_account() -> None:
    for _ in range(LOCKOUT_FAILED_ATTEMPT_LIMIT):
        response = client.post(
            "/login",
            json={"account": "unknown", "password": "wrong-password"},
        )

        assert response.status_code == 401

    response = client.post(
        "/login",
        json={"account": VALID_ACCOUNT, "password": VALID_PASSWORD},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"


def test_login_with_missing_password_returns_422() -> None:
    response = client.post("/login", json={"account": VALID_ACCOUNT})

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "password"]


def test_login_with_empty_account_returns_401() -> None:
    response = client.post(
        "/login",
        json={"account": "", "password": VALID_PASSWORD},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid account or password"}


def test_me_with_valid_token_returns_authenticated_account() -> None:
    token = login_successfully()

    response = client.get("/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == {"account": VALID_ACCOUNT, "authenticated": True}


def test_me_without_token_returns_401() -> None:
    response = client.get("/me")

    assert response.status_code == 401
    assert response.json() == {"detail": "Missing bearer token"}


def test_me_with_invalid_token_returns_401() -> None:
    response = client.get("/me", headers={"Authorization": "Bearer invalid-token"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


def test_me_with_expired_token_returns_401() -> None:
    expired_at = datetime.now(UTC) - timedelta(minutes=1)
    expired_token = jwt.encode(
        {"sub": VALID_ACCOUNT, "exp": expired_at},
        TOKEN_SIGNING_KEY,
        algorithm=TOKEN_ALGORITHM,
    )

    response = client.get("/me", headers={"Authorization": f"Bearer {expired_token}"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Token expired"}


def test_repeated_login_attempts_return_valid_tokens() -> None:
    for _ in range(3):
        token = login_successfully()

        response = client.get("/me", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200
        assert response.json()["authenticated"] is True
