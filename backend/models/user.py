from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), unique=True, nullable=False)

    email = Column(String(255), unique=True, nullable=False, index=True)

    password = Column(String(255), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    plants = relationship(
        "Plant",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    chats = relationship(
        "Chat",
        back_populates="user",
        cascade="all, delete-orphan"
    )