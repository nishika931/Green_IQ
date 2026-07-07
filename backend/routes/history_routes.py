from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.dependencies import get_db, get_current_user
from models.chat import Chat

router = APIRouter(prefix="/history", tags=["History"])


@router.get("/")
def get_history(db: Session = Depends(get_db), user=Depends(get_current_user)):

    chats = db.query(Chat).filter(Chat.user_id == user.id).all()

    return chats