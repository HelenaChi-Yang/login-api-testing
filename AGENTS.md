# AGENTS.md

## Project Purpose

This repository demonstrates backend API validation for a login system using FastAPI, pytest, pytest-html, and GitHub Actions.

The project focuses on API behavior, authentication flow validation, regression testing, CI execution, readable test reporting, and safe AI-assisted development workflow.

## Agent Operating Rules

For every new requirement, the agent must:

1. Read the relevant project files before proposing changes.
2. Restate the requirement as a short implementation plan.
3. Ask clarification questions when the expected behavior, scope, or acceptance criteria are unclear.
4. Keep the scope limited to the requested change.
5. Explain which files will be changed before editing.
6. Make the smallest reasonable implementation change.
7. Add or update tests when behavior changes.
8. Run the test suite after implementation.
9. Fix failures caused by the change.
10. Stop and report a blocker if repeated attempts do not resolve the same failure.

## Requirement Planning Flow

Each requirement should be converted into a ticket-style plan before implementation.

The plan should include:

- Title
- Problem statement
- Expected behavior
- Scope
- Out of scope
- Acceptance criteria
- Test cases to add or update
- Implementation notes
- Definition of done

## Clarification Flow

When a requirement is ambiguous, the agent should ask a small number of targeted questions before coding.

The agent should clarify:

- What user behavior should change
- Which API endpoint or UI behavior is affected
- What response status code or response body is expected
- Whether existing tests should be updated
- Whether the change affects CI, security, or documentation

## Development Flow

The implementation flow is:

1. Inspect current code.
2. Identify the smallest affected area.
3. Update application code.
4. Update or add pytest test cases.
5. Run pytest locally.
6. Generate the pytest-html report.
7. Review changed files.
8. Run a security check before commit or push.
9. Prepare a completion report.

## Default Agent Mode

The default workflow uses one agent with separated responsibility stages:

1. Requirement Analyst: read the ticket, clarify scope, and prepare the implementation plan.
2. Developer: implement the scoped change and update tests.
3. QA Reviewer: review test coverage, run pytest, inspect failures, and verify the HTML report.
4. Release Reporter: summarize the reason for change, solution, test result, security check, and ticket closure readiness.

This mode should be used while the repository is small, the requirement is narrow, and one agent can keep the full context without losing accuracy.

## Future Harness Mode

When the workflow becomes too large for one agent to manage reliably, switch to a harness-style orchestration model.

Harness mode means a coordinator controls the delivery flow and delegates work to specialized agents.

Reusable harness workflow notes and role prompts are stored under `ai-workflow/`.

Suggested roles:

- Harness Coordinator: controls the sequence, validates handoffs, and decides whether a ticket is ready to close.
- Ticket Analyst Agent: reads the ticket and produces scope, acceptance criteria, and test expectations.
- Developer Agent: implements the change according to the approved plan.
- QA Agent: reviews test coverage, runs tests, investigates failures, and verifies the test report.
- Release Reporter Agent: prepares root cause or reason for change, solution summary, test evidence, and closure notes.

Use harness mode when one or more of the following is true:

- The ticket affects multiple areas such as API behavior, frontend behavior, CI, and documentation.
- The implementation requires parallel investigation.
- The test suite becomes large enough that QA review needs a separate context.
- A failure remains unresolved after repeated attempts.
- The agent starts losing track of prior decisions, scope boundaries, or test expectations.
- The user explicitly asks to experience or demonstrate a multi-agent workflow.

Do not switch to harness mode automatically unless the user approves it.

Before switching, the agent should explain:

- Why single-agent mode is no longer enough.
- Which specialized agents are needed.
- What each agent will own.
- What artifacts will be passed between agents.
- How the final result will be verified.

## Testing Standard

The test suite should cover relevant login API behavior, including:

- Successful login
- Invalid credentials
- Missing required fields
- Boundary input validation
- Token validation
- Missing token unauthorized access
- Invalid token unauthorized access
- Expired token unauthorized access
- Repeated login attempts
- Response status codes
- Response body correctness
- Authentication state changes
- Error handling behavior

## CI Standard

GitHub Actions must run the pytest suite on push and pull request.

The workflow should generate an HTML report using pytest-html and upload it as an artifact.

## Security Standard

Before committing or pushing changes, verify that the repository does not include:

- `.env`
- API keys
- GitHub tokens
- JWT signing keys
- Private keys
- Certificates
- Local virtual environments
- Generated reports
- Cache files

Only placeholder configuration such as `.env.example` should be committed.

## Completion Report

After implementation, the agent must report:

- Requirement summary
- Files changed
- Behavior changed
- Test cases added or updated
- Test command used
- Test result
- Report location
- Security check result
- Whether the ticket is ready to close

## Ticket Closure Standard

A ticket can be closed only when:

- Acceptance criteria are satisfied.
- Relevant tests pass.
- The HTML test report is generated.
- Security checks do not identify committed secrets.
- The completion report explains the root cause or reason for change.
- The completion report explains the implemented solution.
