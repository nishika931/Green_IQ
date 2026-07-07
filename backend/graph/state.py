from typing import TypedDict, Optional, Any


class AgentState(TypedDict):
    message: str
    city: Optional[str]

    intent: Optional[str]
    response: Optional[str]

    weather: Optional[Any]
    plant_data: Optional[Any]

    user_id: Optional[int]