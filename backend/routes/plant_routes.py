from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.dependencies import get_db, get_current_user
from models.plant import Plant
from schemas.plant_schema import PlantCreate

router = APIRouter(
    prefix="/plants",
    tags=["Plants"]
)



@router.get("/")
def get_plants(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(Plant).filter(
        Plant.user_id == user.id
    ).all()


@router.post("/")
def add_plant(
    plant: PlantCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    new_plant = Plant(
        user_id=user.id,
        plant_name=plant.plant_name,
        nickname=plant.nickname
    )

    db.add(new_plant)
    db.commit()
    db.refresh(new_plant)

    return {
        "message": "Plant added successfully",
        "plant": new_plant
    }


@router.delete("/{plant_id}")
def delete_plant(
    plant_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    plant = db.query(Plant).filter(
        Plant.id == plant_id,
        Plant.user_id == user.id
    ).first()

    if plant is None:
        raise HTTPException(
            status_code=404,
            detail="Plant not found"
        )

    db.delete(plant)
    db.commit()

    return {
        "message": "Plant deleted successfully"
    }