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

    return get_weather(city)