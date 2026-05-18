# Frontend Dependency Pinning Plan

Purpose: resolve the `ERESOLVE` conflict between `vite` and `@vitejs/plugin-react` observed during local `npm ci`.

Proposed steps:

1. Test run: attempt `npm ci --legacy-peer-deps` in CI (already added in `.github/workflows/ci.yml`).
2. Run `npm outdated` in a clean environment to surface mismatches.
3. Align versions with one of the two approaches:
   - Pin `vite` to a version compatible with the resolved `@vitejs/plugin-react` (e.g., downgrade to a 7.x line), OR
   - Upgrade `@vitejs/plugin-react` to a release that supports `vite@8.x` (preferable if other tooling supports it).
4. Update `package.json` with chosen pins and run `npm ci` in CI to verify.
5. Publish a PR `fix/frontend-deps` with the pinned `package.json` and updated `package-lock.json`.

Notes:
- I did not modify `package.json` automatically to avoid introducing runtime breakages. If you want, I can create the PR that updates `package.json` to either pin `vite` to `^7.3.3` or bump `@vitejs/plugin-react` to a `5.x` release and run tests in CI.
