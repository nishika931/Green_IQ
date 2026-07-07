import os
import requests
from dotenv import load_dotenv

from config.llm import llm

load_dotenv()

PERENUAL_API_KEY = os.getenv("PERENUAL_API_KEY")

BASE_URL = "https://perenual.com/api/v2"


def search_plant(plant_name: str):

    url = f"{BASE_URL}/species-list"

    params = {
        "key": PERENUAL_API_KEY,
        "q": plant_name
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None

    data = response.json()

    if not data.get("data"):
        return None

    return data["data"][0]


def get_plant_details(plant_id: int):

    url = f"{BASE_URL}/species/details/{plant_id}"

    params = {
        "key": PERENUAL_API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None

    return response.json()


def generate_ai_care_guide(details):

    prompt = f"""
You are Green IQ's Plant Care Expert.

Below is real plant information from the Perenual database.

Plant Name:
{details.get("common_name")}

Scientific Name:
{", ".join(details.get("scientific_name", []))}

Family:
{details.get("family")}

Using this information, generate a professional plant care guide.

Return ONLY in this format:

🌿 Plant Name:
🧬 Scientific Name:
🌳 Family:
📝 Description:
☀ Sunlight:
💧 Watering:
🌡 Temperature:
💦 Humidity:
🌱 Soil:
🧪 Fertilizer:
📈 Growth Rate:
🌸 Flowering Season:
🐛 Common Problems:
⭐ Care Level:
🐶 Pet Friendly:
"""

    response = llm.invoke(prompt)

    return response.content


def get_complete_plant_info(plant_name: str):

    plant = search_plant(plant_name)

    if not plant:
        return {
            "success": False,
            "message": "Plant not found."
        }

    details = get_plant_details(plant["id"])

    if not details:
        return {
            "success": False,
            "message": "Unable to fetch details."
        }

    ai_guide = generate_ai_care_guide(details)

    return {

        "success": True,

        "basic_info": {

            "id": details.get("id"),

            "common_name": details.get("common_name"),

            "scientific_name": details.get("scientific_name", []),

            "family": details.get("family"),

            "image": details.get("default_image", {}).get("original_url")

        },

        "ai_care_guide": ai_guide

    }