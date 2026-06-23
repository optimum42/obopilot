# users

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def users_health():
    return {"status": "users endpoint ready"}