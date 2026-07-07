from fastapi import APIRouter
import requests
import os

router = APIRouter(prefix="/plant-info", tags=["Plant Info"])

PERENUAL_API_KEY = os.getenv("PERENUAL_API_KEY")


@router.get("/search")
def search_plants(q: str):

    url = f"https://perenual.com/api/species-list?key={PERENUAL_API_KEY}&q={q}"

    res = requests.get(url)
    return res.json()


@router.get("/details/{plant_id}")
def plant_details(plant_id: int):

    url = f"https://perenual.com/api/species/details/{plant_id}?key={PERENUAL_API_KEY}"

    res = requests.get(url)
    return res.json()