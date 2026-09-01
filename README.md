# Login API Testing

Backend API validation project for a minimal login system built with FastAPI, JWT, pytest, and GitHub Actions.

The project includes a small login page, authentication APIs, token-protected access, automated API tests, and CI test execution.

## Tech Stack

- Python 3.12
- FastAPI
- PyJWT
- pytest
- httpx / FastAPI TestClient
- python-dotenv
- GitHub Actions

## Features

- Static login page served by FastAPI
- `POST /login` for credential validation
- JWT access token generation
- `GET /me` protected by Bearer token authentication
- Error handling for invalid credentials, missing fields, missing tokens, invalid tokens, and expired tokens
- pytest coverage for authentication and regression scenarios
- GitHub Actions workflow for automated API test execution

## API Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/` | Serve the login page |
| `GET` | `/health` | Health check |
| `POST` | `/login` | Validate account and password, then return an access token |
| `GET` | `/me` | Validate Bearer token and return authenticated account state |

## Configuration

Create a local `.env` file:

```text
JWT_SIGNING_KEY=local-development-signing-key
```

The repository includes `.env.example` for required configuration keys.

`.env` is ignored by Git and should not be committed.

## Run Locally

Create a virtual environment:

```powershell
python -m venv .venv
```

Install dependencies:

```powershell
.\.venv\Scripts\python -m pip install -r requirements.txt
```

Start the API:

```powershell
.\.venv\Scripts\python -m uvicorn src.login_api.main:app --reload
```

Open the login page:

```text
http://127.0.0.1:8000/
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Test Account

```text
account: helena
password: password123
```

## Manual API Checks

Successful login:

```powershell
$login = Invoke-RestMethod -Uri http://127.0.0.1:8000/login -Method Post -ContentType "application/json" -Body '{"account":"helena","password":"password123"}'
```

Call the protected endpoint:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/me -Headers @{ Authorization = "Bearer $($login.access_token)" }
```

Invalid credentials:

```powershell
Invoke-WebRequest -Uri http://127.0.0.1:8000/login -Method Post -ContentType "application/json" -Body '{"account":"helena","password":"wrong-password"}' -SkipHttpErrorCheck
```

Missing token:

```powershell
Invoke-WebRequest -Uri http://127.0.0.1:8000/me -SkipHttpErrorCheck
```

## Automated Tests

Run the API test suite:

```powershell
.\.venv\Scripts\python -m pytest
```

Current coverage includes:

- health check
- successful login
- invalid credentials
- missing required fields
- empty account boundary input
- valid token access
- missing token unauthorized access
- invalid token unauthorized access
- expired token unauthorized access
- repeated login attempts
- login page response

## CI

GitHub Actions runs the pytest suite on:

- `push`
- `pull_request`

Workflow file:

```text
.github/workflows/api-tests.yml
```

The workflow also publishes a JUnit XML test report as a downloadable artifact:

```text
pytest-junit-report
```

## Repository Safety

Ignored local files include:

```text
.env
.venv/
docs/
.pytest_cache/
__pycache__/
*.pyc
*.key
*.pem
*.pfx
*.crt
*.cer
```

Only `.env.example` should be committed for configuration reference.
