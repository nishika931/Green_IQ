
from typing import TypedDict, Optional, Any


class AgentState(TypedDict, total=False):
    message: str
    city: Optional[str]
    intent: str
    response: str
    weather: Any
    plant_data: Any
    user_id: int
    memory: str
    context: str
    plant_name: Optional[str]
