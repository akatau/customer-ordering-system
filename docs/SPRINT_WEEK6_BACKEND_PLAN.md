# Backend Sprint 6 Plan: Support & Reporting

**Branch**: `feature/backend-week6-support-reporting`
**Base**: `main`
**Created**: May 13, 2026

## Sprint Goal

Deliver the backend support feature set and analytics reporting endpoints, completing the next phase of the Customer Ordering Sub-system.

## Scope

- Support ticketing system
- Order modification workflow for support staff
- Refund processing integration
- Reporting endpoints for sales, inventory, and customer analytics
- Background task support for report generation and email notifications
- Backend documentation and deployment readiness

## Objectives

1. Implement support ticket models, schemas, and endpoints
2. Create support service logic and access control
3. Add order modification and refund APIs
4. Build reporting services for analytics and export formats
5. Introduce Celery task support for asynchronous report generation
6. Validate all new routes with tests and API documentation
7. Maintain consistency with existing authentication and RBAC

## User Stories

- US-012: As a support user, I want to create and manage customer support tickets.
- US-013: As a support user, I want to modify order items and shipping details for existing orders.
- US-014: As an administrator, I want to process refunds and update order status.
- US-015: As an administrator, I want to view sales, inventory, and customer reports.
- US-016: As an administrator, I want report data exported to CSV for offline analysis.

## Acceptance Criteria

- Ticket CRUD endpoints exist and enforce role-based access
- Orders can be modified with audit logging and recalculated totals
- Refund endpoints validate order state and integrate with payment backend
- Reporting endpoints return accurate metrics for sales, inventory, and customers
- Scheduled report generation and email notification tasks are implemented
- End-to-end tests cover all support and reporting flows
- API documentation is updated for all new endpoints

## Tasks

1. Review `backend/app/api/support.py` and `backend/app/services/support_service.py` for completeness
2. Add support models and schemas if missing (`ticket.py`, `support.py`)
3. Implement `POST /api/v1/support/tickets`, `GET /api/v1/support/tickets`, `PUT /api/v1/support/tickets/{id}`
4. Implement admin support actions: `escalate`, add notes, update priority/status
5. Implement `PUT /api/v1/admin/orders/{id}/modify`
6. Implement `POST /api/v1/admin/orders/{id}/refund`
7. Add reporting endpoints under `admin/reports`
8. Add `Celery` task definitions for report generation and email delivery
9. Update `.github/workflows/ci.yml` if additional dependencies are required
10. Add tests: `test_support.py`, `test_refunds.py`, `test_reporting.py`

## Risks & Mitigations

- Payment refund integration may require API sandbox configuration
  - Mitigation: stub external Stripe calls behind a service layer
- Support role enforcement must not expose admin-only actions
  - Mitigation: validate RBAC at the dependency layer
- Reporting data accuracy depends on historical order metrics
  - Mitigation: implement unit tests for each report calculation

## Notes

- Current `main` is stable and includes admin sprint features.
- This sprint will continue the documented backend engineering process with a clean branch and incremental commits.
- Reference docs:
  - `docs/BACKEND_API_INTEGRATION.md`
  - `docs/DEPLOYMENT_GUIDE.md`
  - `IMPLEMENTATION_LOG.md`
