# PR: Add CI workflow to run backend and frontend tests

Title: ci: add workflow to run backend and frontend tests

Description:
- Adds a GitHub Actions workflow `.github/workflows/ci.yml` that runs backend tests (using an in-memory SQLite DB) and frontend installs/tests (using `--legacy-peer-deps` in CI to avoid peer dependency resolution issues observed locally).

What to verify:
- Workflow file exists at `.github/workflows/ci.yml`.
- Backend job runs `pytest` with `DATABASE_URL=sqlite://`.
- Frontend job installs with `npm ci --legacy-peer-deps` and runs `npm test`.

Notes:
- This PR is intentionally conservative; it does not change production defaults. If the CI needs PostgreSQL, update the workflow to run a Postgres service.
