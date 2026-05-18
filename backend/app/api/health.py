from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["Health"])
def health_check() -> dict:
    return {"status": "ok", "service": "customer_ordering_backend"}


@router.get("/health/", tags=["Health"])
def health_check_slash() -> dict:
    return {"status": "healthy", "service": "customer_ordering_backend"}
