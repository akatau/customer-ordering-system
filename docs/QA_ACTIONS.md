# QA Action Items

This file captures short-term QA tasks and recommended fixes discovered during testing.

- **A1: CI test job**: Create a CI workflow that runs backend tests in a clean environment (Linux) and documents system-level dependencies. Priority: High. Owner: DevOps/Backend.
- **A2: Dependency docs**: Document how to install `pg_config`/Postgres dev tools on supported development platforms, or provide a dev container. Priority: Medium. Owner: Backend.
- **A3: Address deprecations**: Triage and schedule changes for Pydantic v2 migration, replacing FastAPI `on_event` with lifespan, and using timezone-aware datetimes. Priority: Low-Medium. Owner: Backend.
- **A4: Frontend test run**: Attempt to run frontend tests and capture results; if environment lacks Node, add CI job for frontend. Priority: Medium. Owner: Frontend.
- **A5: Test reproducibility**: Add a short `CONTRIBUTING.md` or `DEVELOPER_QUICK_START.md` section describing how to run tests locally (including the `DATABASE_URL='sqlite://'` workaround). Priority: High. Owner: Maintainers.

Each action should be converted to a tracked issue (e.g., in GitHub) with acceptance criteria and a test to validate the fix.
