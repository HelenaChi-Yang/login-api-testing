# AI-Assisted Development Workflow

This directory defines the harness-style workflow used to manage requirements, implementation, testing, and release readiness for this repository.

## Current Mode

The current workflow uses a pilot harness model:

1. Harness Coordinator manages the overall flow in the main thread.
2. Ticket Analyst Agent prepares scope, acceptance criteria, and test expectations.
3. Developer work is handled by the main coordinator to avoid overlapping code edits.
4. QA Reviewer Agent performs independent verification after implementation.
5. Harness Coordinator prepares the completion report and closure notes.

## Why Developer Work Stays in the Main Thread

This repository is intentionally small. Keeping code edits in the main thread reduces file conflict risk and makes each implementation step easier to explain and review.

Developer work can be delegated to a separate agent later when:

- The change has a clearly isolated file scope.
- Multiple implementation tasks can happen in parallel.
- The repository has enough tests and structure to support safe integration.

## Ticket Flow

For each requirement:

1. Convert the requirement into a ticket-style plan.
2. Ask clarification questions if the requirement is unclear.
3. Confirm the plan before implementation.
4. Implement the smallest reasonable change.
5. Add or update tests.
6. Run pytest with pytest-html.
7. Ask QA Reviewer Agent to review behavior and coverage.
8. Fix failures or coverage gaps.
9. Run security checks.
10. Prepare the ticket completion report.

## Agent Handoff Artifacts

Each agent should produce a concise handoff artifact.

Ticket Analyst output:

- Title
- Problem statement
- Scope
- Out of scope
- Acceptance criteria
- Test cases
- Clarification questions if needed

QA Reviewer output:

- Coverage assessment
- Missing or weak test cases
- Risk notes
- Test command recommendation
- Release readiness recommendation

Completion report output:

- Requirement summary
- Files changed
- Behavior changed
- Tests added or updated
- Test result
- Report location
- Security check result
- Closure recommendation
