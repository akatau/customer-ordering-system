# Customer Ordering Sub-system

A comprehensive, scalable e-commerce ordering platform built with modern technologies and architectural best practices.

## Overview

The Customer Ordering Sub-system is a complete e-commerce solution that handles customer registration, product browsing, shopping cart management, secure payments, order processing, and administrative functions. Built with a focus on architectural integrity, security, and scalability.

## Features

### Customer Features
- User registration and authentication
- Product catalog browsing with search and filters
- Shopping cart management
- Secure checkout with multiple payment methods
- Order tracking and history
- Product reviews and ratings
- Password recovery

### Administrative Features
- Product management (CRUD operations)
- Order management and status updates
- User administration
- Sales reporting and analytics
- User activity monitoring
- Invoice generation

### Support Features
- Customer inquiry ticketing
- Order modification requests
- Refund processing
- Support escalation workflows

## Technology Stack

### Backend
- **Framework**: FastAPI (Python async web framework)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens with bcrypt hashing
- **Task Queue**: Celery with Redis
- **External APIs**: Stripe (payments), SendGrid (email)

### Frontend
- **Framework**: React 18 with TypeScript
- **UI Library**: Material-UI (MUI)
- **State Management**: Zustand
- **Forms**: React Hook Form with Zod validation
- **HTTP Client**: Axios
- **Build Tool**: Vite

### DevOps & Testing
- **Containerization**: Docker & Docker Compose
- **Orchestration**: Kubernetes
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus & Grafana
- **Testing**: pytest (backend), Jest + React Testing Library (frontend)
- **Code Quality**: Black, isort, flake8, mypy, ESLint

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 20+ (for frontend development)
- Python 3.11+ (for backend development)
- Nix (optional, for shell.nix environment)

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd customer-ordering-system
   ```

2. **Start development environment**
   ```bash
   make setup-dev
   ```

   This will:
   - Install all dependencies
   - Start PostgreSQL and Redis with Docker
   - Run database migrations
   - Start backend on http://localhost:8000
   - Start frontend on http://localhost:3000

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Database Admin: Use your preferred PostgreSQL client

### Manual Setup

If you prefer manual setup:

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
yarn install
yarn dev
```

## Project Structure

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed directory layout and explanations.

## API Documentation

The backend provides comprehensive API documentation at `/docs` when running. Key endpoints include:

- `POST /api/v1/auth/register` - User registration
- `GET /api/v1/products` - Product catalog
- `POST /api/v1/orders` - Create order
- `GET /api/v1/orders/{id}` - Order details
- `POST /api/v1/admin/products` - Create product (admin)

## Development Workflow

### Code Quality
```bash
# Format code
make format

# Run linters
make lint

# Run tests
make test

# Run everything
make format lint test
```

### Database Management
```bash
# Create migration
make migrate msg="add user preferences"

# Run migrations
make migrate-up

# Reset database (WARNING: destroys data)
make db-reset
```

### Docker Operations
```bash
# Start all services
make docker-up

# Stop all services
make docker-down

# View logs
make logs-backend
make logs-frontend
```

## Deployment

### Local Production
```bash
# Build and run with Docker Compose
docker-compose -f docker/docker-compose.prod.yml up -d
```

### Kubernetes
```bash
# Deploy to Kubernetes cluster
kubectl apply -f kubernetes/
```

### CI/CD
The project includes GitHub Actions workflows for:
- Automated testing on pull requests
- Security scanning
- Deployment to staging/production environments

## Configuration

### Environment Variables

Create `.env` files in `backend/` and `frontend/` directories:

**Backend (.env)**
```env
DATABASE_URL=postgresql://user:password@localhost/customer_ordering
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key
STRIPE_SECRET_KEY=sk_test_...
SENDGRID_API_KEY=SG...
```

**Frontend (.env)**
```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

## Testing

### Backend Tests
```bash
cd backend
pytest -v --cov=app
```

### Frontend Tests
```bash
cd frontend
yarn test
```

### Integration Tests
```bash
# Run with Docker Compose
docker-compose -f docker/docker-compose.test.yml up --abort-on-container-exit
```

## Monitoring

The system includes comprehensive monitoring:
- **Application Metrics**: Response times, error rates, throughput
- **Infrastructure**: CPU, memory, database connections
- **Business Metrics**: Order volumes, conversion rates

Access Grafana at http://localhost:3001 (when running with monitoring stack).

## Security

- **Authentication**: JWT with secure storage
- **Authorization**: Role-based access control
- **Data Protection**: Encryption at rest and in transit
- **Input Validation**: Comprehensive validation with Pydantic/Zod
- **Rate Limiting**: API rate limiting to prevent abuse
- **Security Headers**: CORS, CSP, HSTS configured

## Performance

- **Response Times**: <2 seconds for 95% of requests
- **Concurrent Users**: Supports 1000+ concurrent users
- **Scalability**: Horizontal scaling with Kubernetes
- **Caching**: Redis caching for frequently accessed data
- **Database Optimization**: Indexed queries and connection pooling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Ensure all checks pass
5. Submit a pull request

### Code Standards
- Follow PEP 8 for Python
- Use TypeScript strict mode
- Write comprehensive tests
- Update documentation

## Documentation

All documentation is in the `docs/` directory:
- [System Overview](docs/system_overview.md)
- [Requirements](docs/requirements.md)
- [API Contracts](docs/api_contracts.md)
- [Final Design](docs/final_design.md)

**Team Implementation**:
- [Team Work Distribution](TEAM_WORK_DISTRIBUTION.md) - Detailed task breakdown for 3-person team
- [Developer Quick Start](DEVELOPER_QUICK_START.md) - Quick reference guide for each developer
- [Project Structure](PROJECT_STRUCTURE.md) - Directory layout and file organization

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the API documentation at `/docs`

## Roadmap

- [ ] Mobile app development
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Integration with third-party marketplaces
- [ ] AI-powered product recommendations
- [ ] Real-time inventory synchronization
