# PR: Fix frontend dependency conflicts by pinning `vite` or upgrading plugin

Title: fix(frontend): pin vite to ^7.3.3 to resolve peer dependency conflicts

Description:
- Pin `vite` to `^7.3.3` in `frontend/package.json` to resolve a peer dependency conflict between `vite@8.x` and `@vitejs/plugin-react@4.7.0` observed during local `npm ci`.
- Update `package-lock.json` accordingly.

What to verify:
- `frontend/package.json` contains `vite: "^7.3.3"`.
- `npm ci --legacy-peer-deps` completes in CI and `npm test` runs successfully.

Alternative:
- Instead of downgrading `vite`, consider upgrading `@vitejs/plugin-react` to a version that supports `vite@8.x`. This PR chooses the conservative approach; happy to open a follow-up PR for the alternative.
