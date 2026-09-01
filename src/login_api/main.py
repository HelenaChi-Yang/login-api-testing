import os
from datetime import UTC, datetime, timedelta
from pathlib import Path

import jwt
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="Login API Testing")

FRONTEND_PATH = Path(__file__).resolve().parents[2] / "frontend" / "index.html"
VALID_ACCOUNT = "helena"
VALID_PASSWORD = "password123"
TOKEN_SIGNING_KEY = os.getenv("JWT_SIGNING_KEY")
TOKEN_ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

if TOKEN_SIGNING_KEY is None:
    raise RuntimeError("JWT_SIGNING_KEY environment variable is required")


class LoginRequest(BaseModel):
    account: str
    password: str


class LoginResponse(BaseModel):
    message: str
    account: str
    access_token: str
    token_type: str


class MeResponse(BaseModel):
    account: str
    authenticated: bool


def create_access_token(account: str) -> str:
    expires_at = datetime.now(UTC) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload = {"sub": account, "exp": expires_at}

    return jwt.encode(payload, TOKEN_SIGNING_KEY, algorithm=TOKEN_ALGORITHM)


def get_account_from_token(authorization: str | None) -> str:
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
        )

    token = authorization.removeprefix("Bearer ").strip()

    try:
        payload = jwt.decode(token, TOKEN_SIGNING_KEY, algorithms=[TOKEN_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    account = payload.get("sub")
    if account != VALID_ACCOUNT:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    return account


@app.get("/", response_class=FileResponse)
def login_page() -> FileResponse:
    return FileResponse(FRONTEND_PATH)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/login", response_model=LoginResponse)
def login(request: LoginRequest) -> LoginResponse:
    if request.account != VALID_ACCOUNT or request.password != VALID_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid account or password",
        )

    return LoginResponse(
        message="Login successful",
        account=request.account,
        access_token=create_access_token(request.account),
        token_type="Bearer",
    )


@app.get("/me", response_model=MeResponse)
def me(authorization: str | None = Header(default=None)) -> MeResponse:
    account = get_account_from_token(authorization)

    return MeResponse(account=account, authenticated=True)
