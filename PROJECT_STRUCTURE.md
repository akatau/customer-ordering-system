# Project Structure

```
customer-ordering-system/
├── docs/                          # Documentation
│   ├── README.md                 # Documentation index
│   ├── system_overview.md        # System overview
│   ├── actors.md                 # Actor classification
│   ├── requirements.md           # Requirements specification
│   ├── traceability.md           # Traceability matrix
│   ├── user_stories.md           # User stories
│   ├── gherkin.md                # Gherkin scenarios
│   ├── refinement.md             # QA audit and refinements
│   ├── uml.md                    # System and activity diagrams
│   ├── api_contracts.md          # API specifications
│   ├── key_decisions.md          # Architectural decisions
│   ├── refined_summary.md        # Refinement summary
│   └── final_design.md           # Final implementation plan
├── backend/                      # Python FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py               # FastAPI application
│   │   ├── config.py             # Configuration settings
│   │   ├── database.py           # Database connection
│   │   ├── models/               # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── product.py
│   │   │   ├── order.py
│   │   │   ├── cart.py
│   │   │   ├── review.py
│   │   │   └── ticket.py
│   │   ├── schemas/              # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── product.py
│   │   │   ├── order.py
│   │   │   └── auth.py
│   │   ├── api/                  # API routes
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── products.py
│   │   │   ├── cart.py
│   │   │   ├── orders.py
│   │   │   ├── reviews.py
│   │   │   ├── admin.py
│   │   │   └── support.py
│   │   ├── core/                 # Core functionality
│   │   │   ├── __init__.py
│   │   ├── services/             # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── product_service.py
│   │   │   ├── order_service.py
│   │   │   ├── payment_service.py
│   │   │   ├── shipping_service.py
│   │   │   └── email_service.py
│   │   ├── utils/                # Utilities
│   │   │   ├── __init__.py
│   │   │   ├── security.py
│   │   │   └── pagination.py
│   │   └── tasks/                # Celery tasks
│   │       ├── __init__.py
│   │       └── email_tasks.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_products.py
│   │   ├── test_orders.py
│   │   └── test_integration.py
│   ├── alembic/                  # Database migrations
│   │   ├── versions/
│   │   └── env.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                     # React TypeScript frontend
│   ├── public/
│   │   ├── index.html
│   │   └── assets/
│   ├── src/
│   │   ├── components/           # Reusable components
│   │   │   ├── common/
│   │   │   ├── auth/
│   │   │   ├── products/
│   │   │   ├── cart/
│   │   │   ├── orders/
│   │   │   └── admin/
│   │   ├── pages/                # Page components
│   │   │   ├── Home.tsx
│   │   │   ├── Login.tsx
│   │   │   ├── Register.tsx
│   │   │   ├── Products.tsx
│   │   │   ├── ProductDetail.tsx
│   │   │   ├── Cart.tsx
│   │   │   ├── Checkout.tsx
│   │   │   ├── OrderHistory.tsx
│   │   │   ├── AdminDashboard.tsx
│   │   │   └── SupportDashboard.tsx
│   │   ├── hooks/                # Custom hooks
│   │   │   ├── useAuth.ts
│   │   │   ├── useProducts.ts
│   │   │   └── useCart.ts
│   │   ├── stores/               # Zustand stores
│   │   │   ├── authStore.ts
│   │   │   ├── cartStore.ts
│   │   │   └── uiStore.ts
│   │   ├── utils/                # Utilities
│   │   │   ├── api.ts
│   │   │   ├── constants.ts
│   │   │   └── helpers.ts
│   │   ├── types/                # TypeScript types
│   │   │   ├── index.ts
│   │   │   └── api.ts
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── tests/
│   │   ├── setup.ts
│   │   ├── components/
│   │   └── pages/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── Dockerfile
├── docker/                       # Docker configurations
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   └── nginx.conf
├── kubernetes/                   # Kubernetes manifests
│   ├── backend-deployment.yml
│   ├── frontend-deployment.yml
│   ├── database-statefulset.yml
│   ├── redis-deployment.yml
│   ├── ingress.yml
│   └── configmaps.yml
├── .github/workflows/            # CI/CD pipelines
│   ├── backend-ci.yml
│   ├── frontend-ci.yml
│   └── deploy.yml
├── monitoring/                   # Monitoring configurations
│   ├── prometheus.yml
│   ├── grafana-dashboards/
│   └── alertmanager.yml
├── scripts/                      # Utility scripts
│   ├── setup-dev.sh
│   ├── backup-db.sh
│   └── migrate-db.sh
├── shell.nix                     # Nix environment
├── requirements.txt              # Python dependencies
├── package.json                  # Node dependencies
├── docker-compose.yml            # Local development
├── Makefile                      # Common commands
├── README.md                     # Project README
└── .gitignore
```

## Directory Explanations

### Backend Structure
- **app/**: Main application code with clear separation of concerns
- **models/**: Database models using SQLAlchemy
- **schemas/**: API request/response validation with Pydantic
- **api/**: FastAPI route handlers
- **services/**: Business logic layer
- **core/**: Configuration and shared components
- **utils/**: Helper functions and utilities
- **tasks/**: Asynchronous background tasks

### Frontend Structure
- **components/**: Reusable UI components organized by feature
- **pages/**: Top-level page components
- **hooks/**: Custom React hooks for data fetching and state
- **stores/**: Global state management with Zustand
- **utils/**: API clients and helper functions
- **types/**: TypeScript type definitions

### Infrastructure
- **docker/**: Container configurations for different environments
- **kubernetes/**: Production deployment manifests
- **.github/workflows/**: Automated CI/CD pipelines
- **monitoring/**: Observability stack configurations
- **scripts/**: Development and maintenance utilities

This structure ensures scalability, maintainability, and clear separation of concerns across the entire system.
