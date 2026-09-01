# Project Brief

`login-api-testing` is a compact backend API validation project focused on authentication behavior, JWT-protected endpoints, regression coverage, and CI execution.

## Objectives

- Provide a minimal login page backed by FastAPI endpoints.
- Validate login and token flows through pytest-based API tests.
- Cover positive, negative, boundary, and unauthorized access scenarios.
- Run the backend API test suite automatically with GitHub Actions.
- Keep local configuration and secrets out of source control.

## Scope

Included:

- FastAPI backend
- static login page served by the API
- JWT access token creation and validation
- pytest API test suite
- GitHub Actions CI workflow
- local `.env` configuration with `.env.example`

Excluded:

- database persistence
- cloud deployment
- browser UI automation
- performance testing
- third-party authentication provider

## Quality Focus

The test suite validates:

- request payload handling
- response status codes
- response body correctness
- invalid credential handling
- required field validation
- token validation
- unauthorized access behavior
- expired token handling
- repeated login regression coverage

## Security Focus

- `.env` is ignored by Git.
- `.env.example` documents required configuration without exposing real secrets.
- JWT signing key is read from `JWT_SIGNING_KEY`.
- CI uses a test-only signing key defined in the workflow environment.
