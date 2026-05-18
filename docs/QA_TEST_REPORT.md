# QA Test Report

- **Date:** 2026-05-18
- **Environment:** Windows, project root `d:/darksoulsIII/customer-ordering-system`

## Actions performed

- Configured project Python virtual environment (venv) for `backend/`.
- Ran backend test suite with an in-memory SQLite DB to avoid system Postgres dependencies.

## Commands run

```powershell
$Env:DATABASE_URL='sqlite://'
cd backend
d:/darksoulsIII/customer-ordering-system/.venv/Scripts/python.exe -m pytest -q
```

## Test summary

- Total tests: 26
- Passed: 26
- Failed: 0
- Warnings: 145
- Runtime: ~4.11s

Pytest summary line:

```
26 passed, 145 warnings in 4.11s
```

## Notable warnings and observations

- The codebase emits several deprecation warnings (Pydantic, FastAPI `on_event`, SQLAlchemy datetime usage). These are low-priority but should be scheduled for future maintenance.
- Several service modules use `datetime.utcnow()` which is deprecated in the current SQLAlchemy/Python environment — migrate to timezone-aware datetimes.

## Dependency issue encountered

- Attempted to install `requirements.txt` into the venv; installation failed when building `psycopg2-binary` due to missing `pg_config` (PostgreSQL dev headers/tools) on the host:

```
Error: pg_config executable not found.
pg_config is required to build psycopg2 from source.
```

Workaround used: run tests with `DATABASE_URL='sqlite://'` so `app.database` uses SQLite and tests run in-memory.

## Recommendations

- Add a CI job that runs backend tests in a clean environment and documents any OS-level dependencies (e.g., PostgreSQL dev libs) required to build native wheels.
- Consider replacing `psycopg2-binary` with a wheel-friendly pinned version or ensure CI images include `pg_config` if PostgreSQL is required.
- Address deprecation warnings over time (Pydantic v2 migration, FastAPI lifespan handlers, timezone-aware datetimes).

## Next steps

- Run frontend tests (separately) and add their results to this report.
- Create a short QA action list with items prioritised by risk and effort (see `QA_ACTIONS.md`).

## Frontend test attempt

- Attempted to run frontend tests via the `frontend/` package. Installation failed due to dependency resolution conflicts between `vite` and `@vitejs/plugin-react` on the local machine. The `npm ci` step returned an ERESOLVE conflict. Example error:

```
npm error ERESOLVE could not resolve
... Could not resolve dependency: peer vite@"^4.2.0 || ^5.0.0 || ^6.0.0 || ^7.0.0" from @vitejs/plugin-react@4.7.0
```

Recommendations:

- Try `npm ci --legacy-peer-deps` or update `package.json` to align `vite` and plugin versions.
- Run frontend CI in a container or CI runner with a supported Node version and a clean cache to reproduce and fix dependency resolution.
- If desired, I can open a PR that pins compatible `vite`/plugin versions and attempts a green install in CI.

