from fastapi import APIRouter

from app.core.health import health_response

router = APIRouter()


@router.get("/health")
def health():
    return health_response()
