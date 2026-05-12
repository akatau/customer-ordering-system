# shell.nix

# Reproducible development environment for Customer Ordering Sub-system
# Backend: Python with FastAPI and all dependencies for complete implementation

{ pkgs ? import <nixpkgs> { config = { allowUnfree = true; }; } }:

let
  python = pkgs.python311;  # Use Python 3.11 for stability and performance
in

pkgs.mkShell {
  buildInputs = [
    python

    # Python packages for backend development
    python.pkgs.pip
    python.pkgs.virtualenv  # For isolated environment management
    python.pkgs.setuptools
    python.pkgs.wheel

    # Development tools
    pkgs.git  # Version control
    pkgs.docker  # Containerization for deployment
    pkgs.postgresql  # Database (can be swapped for other DBs)
    pkgs.redis  # For caching and task queue

    # Code quality and testing
    python.pkgs.black  # Code formatter
    python.pkgs.isort  # Import sorter
    python.pkgs.flake8  # Linter
    python.pkgs.mypy  # Type checker
    python.pkgs.pytest  # Testing framework
    python.pkgs.coverage  # Test coverage
    python.pkgs.pytest-asyncio  # Async testing
    python.pkgs.pytest-cov  # Coverage reporting

    # Additional tools for full implementation
    pkgs.nodejs_20  # For frontend development (if needed)
    pkgs.yarn  # Package manager for frontend
    pkgs.kubectl  # Kubernetes CLI
    pkgs.kubernetes-helm  # Helm for Kubernetes packages
    pkgs.terraform  # Infrastructure as code
    pkgs.awscli2  # AWS CLI for cloud deployment
    pkgs.postman  # API testing tool

    # Documentation
    python.pkgs.sphinx  # Documentation generator
    pkgs.mdbook  # For additional docs if needed
  ];

  shellHook = ''
    echo "Customer Ordering Sub-system Development Environment"
    echo "Python version: $(python --version)"
    echo "Node.js version: $(node --version)"
    echo "Docker version: $(docker --version)"
    echo "PostgreSQL available: $(which psql)"
    echo "Redis available: $(which redis-cli)"
    echo ""
    echo "To create a virtual environment:"
    echo "  python -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    echo ""
    echo "For frontend development:"
    echo "  cd frontend"
    echo "  yarn install"
    echo "  yarn dev"
    echo ""
    echo "Available tools:"
    echo "  Python: black, isort, flake8, mypy, pytest, coverage"
    echo "  Docker: docker, docker-compose"
    echo "  Kubernetes: kubectl, helm"
    echo "  Cloud: awscli, terraform"
    echo "  API Testing: postman"
  '';

  # Environment variables
  PYTHONPATH = "./src";
  DATABASE_URL = "postgresql://localhost/customer_ordering_dev";
  REDIS_URL = "redis://localhost:6379";
  SECRET_KEY = "dev-secret-key-change-in-production";
}
