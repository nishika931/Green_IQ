import os
import requests
from dotenv import load_dotenv

from config.llm import llm

load_dotenv()

PERENUAL_API_KEY = os.getenv("PERENUAL_API_KEY")

BASE_URL = "https://perenual.com/api/v2"

REQUEST_TIMEOUT = 10

def search_plant(plant_name: str):

    try:

        url = f"{BASE_URL}/species-list"

        params = {
            "key": PERENUAL_API_KEY,
            "q": plant_name
        }

        response = requests.get(
            url,
            params=params,
            timeout=REQUEST_TIMEOUT
        )


        if response.status_code != 200:
            return None


        data = response.json()


        if not data.get("data"):
            return None


        return data["data"][0]


    except Exception as e:

        print("Perenual Search Error:", e)
        return None



# -----------------------------
# GET COMPLETE PLANT DETAILS
# -----------------------------
def get_plant_details(plant_id: int):

    try:

        url = f"{BASE_URL}/species/details/{plant_id}"

        params = {
            "key": PERENUAL_API_KEY
        }


        response = requests.get(
            url,
            params=params,
            timeout=REQUEST_TIMEOUT
        )


        if response.status_code != 200:
            return None


        return response.json()


    except Exception as e:

        print("Perenual Details Error:", e)
        return None



# -----------------------------
# AI CARE GUIDE
# -----------------------------
def generate_ai_care_guide(details):

    try:

        prompt = f"""

You are Green IQ Plant Care Expert.

Use this real plant data:

Plant:
{details.get("common_name")}

Scientific Name:
{details.get("scientific_name")}

Family:
{details.get("family")}


Create a simple plant care guide.

Format:

🌿 Plant Name:
🧬 Scientific Name:
🌳 Family:

📝 Description:

☀ Sunlight:

💧 Watering:

🌱 Soil:

🌡 Temperature:

💦 Humidity:

🧪 Fertilizer:

🐛 Common Problems:

⭐ Care Level:

🐶 Pet Friendly:

"""


        response = llm.invoke(prompt)

        return response.content


    except Exception as e:

        return f"Unable to generate care guide: {str(e)}"


def get_complete_plant_info(plant_name: str):

    if not PERENUAL_API_KEY:

        return {
            "success": False,
            "message": "Perenual API key missing."
        }


    plant = search_plant(plant_name)


    if not plant:

        corrected_name = plant_name.lower()

        corrections = {
            "rattle snake plant": "rattlesnake plant",
            "snake plant": "snake plant",
            "money plants": "money plant"
        }


        corrected_name = corrections.get(
            corrected_name,
            corrected_name
        )


        plant = search_plant(corrected_name)



    if not plant:

        return {
            "success": False,
            "message": f"Plant '{plant_name}' not found."
        }



    details = get_plant_details(
        plant["id"]
    )


    if not details:

        return {
            "success": False,
            "message": "Unable to fetch plant details."
        }



    ai_guide = generate_ai_care_guide(details)



    return {

        "success": True,


        "basic_info": {

            "id": details.get("id"),

            "common_name": details.get(
                "common_name"
            ),

            "scientific_name": details.get(
                "scientific_name",
                []
            ),

            "family": details.get(
                "family"
            ),


            "image": details.get(
                "default_image",
                {}
            ).get(
                "original_url"
            )
        },


        "ai_care_guide": ai_guide

    }