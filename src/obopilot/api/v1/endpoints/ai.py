from datetime import datetime
from fastapi import APIRouter, status

from obopilot.services import ai_service
from obopilot.models.positioning import TargetGroupInput

router = APIRouter()


@router.get("/health")
def ai_health():
    return {"status": "ai endpoint ready"}


@router.post("/target-groups",
    response_model = dict,
    status_code=status.HTTP_201_CREATED,
)
def get_target_group(
    target_group_input: TargetGroupInput,
):
    offer = target_group_input.offer
    uniqueness = target_group_input.uniqueness
    target_groups = ai_service.generate_target_groups(
        offer=offer,
        uniqueness=uniqueness,
        count=target_group_input.count)
    return {
        "offer": offer,
        "uniqueness": uniqueness,
        "target_groups": target_groups,
        "datum": datetime.now(),
    }