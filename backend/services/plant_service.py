from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.plant import Plant
from models.user import User
from schemas.plant_schema import PlantCreate, PlantUpdate


def add_plant(
    plant: PlantCreate,
    current_user: User,
    db: Session
):
    """
    Add a new plant for the logged-in user.
    """

    new_plant = Plant(
        user_id=current_user.id,
        plant_name=plant.plant_name,
        nickname=plant.nickname
    )

    db.add(new_plant)
    db.commit()
    db.refresh(new_plant)

    return {
        "message": "Plant added successfully.",
        "plant": new_plant
    }


def get_my_plants(
    current_user: User,
    db: Session
):
    """
    Get all plants of the logged-in user.
    """

    plants = (
        db.query(Plant)
        .filter(Plant.user_id == current_user.id)
        .order_by(Plant.created_at.desc())
        .all()
    )

    return plants


def update_plant(
    plant_id: int,
    plant_data: PlantUpdate,
    current_user: User,
    db: Session
):
    """
    Update a plant.
    """

    plant = (
        db.query(Plant)
        .filter(
            Plant.id == plant_id,
            Plant.user_id == current_user.id
        )
        .first()
    )

    if not plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plant not found."
        )

    update_data = plant_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(plant, key, value)

    db.commit()
    db.refresh(plant)

    return {
        "message": "Plant updated successfully.",
        "plant": plant
    }


def delete_plant(
    plant_id: int,
    current_user: User,
    db: Session
):
    """
    Delete a plant.
    """

    plant = (
        db.query(Plant)
        .filter(
            Plant.id == plant_id,
            Plant.user_id == current_user.id
        )
        .first()
    )

    if not plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plant not found."
        )

    db.delete(plant)
    db.commit()

    return {
        "message": "Plant deleted successfully."
    }