from fastapi import APIRouter
from pydantic import BaseModel

from services.perenual_service import get_complete_plant_info

router = APIRouter(
    prefix="/plant-ai",
    tags=["Plant AI"]
)


class PlantRequest(BaseModel):
    plant_name: str


@router.post("/details")
def plant_details(request: PlantRequest):

    return get_complete_plant_info(request.plant_name)