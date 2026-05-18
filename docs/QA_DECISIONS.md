# QA Decisions and Notes

This document records decisions made during the QA run and rationale.

- Decision: Use an in-memory SQLite DB for unit tests by default. Rationale: avoids requiring OS-level Postgres build tools during local runs and CI, speeds up tests.
- Decision: Do not modify application defaults to SQLite in production. Rationale: production uses PostgreSQL; tests should be isolated via environment overrides.
- Decision: Document environment workarounds rather than changing production code. Rationale: minimize risk to runtime behavior while enabling developer productivity.

Notes:

- The immediate blocker was `psycopg2` build requiring `pg_config`. Installing `psycopg2-binary` or ensuring CI images contain PostgreSQL dev tools are both valid strategies; choose based on CI/OS constraints.
