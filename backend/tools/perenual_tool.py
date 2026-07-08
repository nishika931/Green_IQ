from langchain_core.tools import tool

from services.perenual_service import get_complete_plant_info


@tool
def plant_info_tool(plant_name: str) -> dict:
    """
    Fetch detailed information about a plant using the Perenual API.
    """

    try:
        return get_complete_plant_info(plant_name)

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }