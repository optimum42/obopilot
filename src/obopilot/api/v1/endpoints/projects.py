# projects

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def projects_health():
    return {"status": "projects endpoint ready"}