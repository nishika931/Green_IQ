from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class PlantCreate(BaseModel):
    plant_name: str = Field(..., min_length=2, max_length=150)
    nickname: Optional[str] = Field(default=None, max_length=100)


class PlantUpdate(BaseModel):
    plant_name: Optional[str] = Field(default=None, min_length=2, max_length=150)
    nickname: Optional[str] = Field(default=None, max_length=100)
    scientific_name: Optional[str] = None
    watering_frequency: Optional[str] = None
    sunlight: Optional[str] = None


class PlantResponse(BaseModel):
    id: int
    user_id: int
    plant_name: str
    nickname: Optional[str] = None
    scientific_name: Optional[str] = None
    watering_frequency: Optional[str] = None
    sunlight: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)