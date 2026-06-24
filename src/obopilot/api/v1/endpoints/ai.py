from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def ai_health():
    return {"status": "ai endpoint ready"}