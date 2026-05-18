# Frontend Sprint 3 Notes

## Scope

This sprint pass focused on the next frontend optimization slice identified in the implementation log and sprint 2 follow-ups:

- Add a global error boundary around the routed app shell
- Lazy-load all routed pages with a skeleton fallback
- Keep the existing backend-backed admin route and auth guards intact

## What Changed

### Route Resilience

- Added a reusable error boundary at [frontend/src/components/AppErrorBoundary.tsx](../frontend/src/components/AppErrorBoundary.tsx).
- Wrapped the application shell in that boundary so render failures surface with a recovery message instead of a blank screen.
- Kept recovery actions simple: reload the app or go back to `/`.

### Bundle Splitting

- Converted all page routes in [frontend/src/App.tsx](../frontend/src/App.tsx) to `React.lazy` imports.
- Added a suspense fallback skeleton so route transitions stay visually stable while chunks load.
- Left the header, footer, and auth shell eager-loaded so navigation remains available immediately.

### Test Adjustment

- Updated the app smoke test in [frontend/src/tests/App.test.tsx](../frontend/src/tests/App.test.tsx) to wait for the lazy-loaded header.

## Decisions

- I kept the error handling at the shell level rather than introducing per-page boundaries because the current risk is route-level render failure, not a single isolated widget.
- The lazy route split includes the admin page as well, which keeps the public bundle smaller without changing the backend integration model.
- I did not change the existing React Router structure or auth guards; this sprint was about resilience and loading behavior, not route semantics.

## Validation

- `npm.cmd test -- --run src/tests/App.test.tsx`
- `npm.cmd test -- --run`
- `npm.cmd run type-check`
- `npm.cmd run build`

## Follow-Up

- Address the React Router v7 future-flag warnings in a deliberate compatibility pass.
- Add richer loading states only where a route needs more than the current skeleton fallback.
- Continue keeping new route work lazy-loaded so the initial bundle does not drift back up.