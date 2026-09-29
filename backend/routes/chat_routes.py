from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.dependencies import get_db, get_current_user
from models.chat import Chat
from schemas.chat import ChatRequest
from graph.graph import run_graph
from graph.state import AgentState


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    recent_chats = (
        db.query(Chat)
        .filter(Chat.user_id == user.id)
        .order_by(Chat.created_at.desc())
        .limit(4)
        .all()
    )

    recent_chats.reverse()

    memory_text = "\n".join(
        f"{chat.role}: {chat.message}"
        for chat in recent_chats
    )

    state: AgentState = {
        "message": request.message,
        "city": request.city,
        "intent": None,
        "response": None,
        "weather": None,
        "plant_data": None,
        "plant_name": None,
        "user_id": user.id,
        "context": None,
        "memory": memory_text
    }

    result = run_graph(state)

    response = result["response"]

    db.add(
        Chat(
            user_id=user.id,
            role="user",
            message=request.message
        )
    )

    db.add(
        Chat(
            user_id=user.id,
            role="assistant",
            message=response
        )
    )

    db.commit()

    return {
        "response": response,
        "intent": result.get("intent")
    }


@router.get("/history")
def history(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    return (
        db.query(Chat)
        .filter(Chat.user_id == user.id)
        .order_by(Chat.created_at.asc())
        .all()
    )
