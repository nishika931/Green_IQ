from langchain_core.tools import tool

from services.weather_service import get_weather


@tool
def weather_tool(city: str) -> dict:
    """
    Get current weather information for a city.

    Args:
        city: Name of the city.

    Returns:
        Dictionary containing weather information.
    """

    try:
        weather = get_weather(city)

        if not weather:
            return {
                "success": False,
                "message": "Weather data not found."
            }

        return weather

    except Exception as e:
        return {
            "success": False,
            "message": f"Weather service error: {str(e)}"
        }