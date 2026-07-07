from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from config.database import Base


class Plant(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

   
    nickname = Column(String(100), nullable=True)

  
    plant_name = Column(String(150), nullable=False)

    scientific_name = Column(String(150), nullable=True)

    watering_frequency = Column(String(100), nullable=True)

    sunlight = Column(String(100), nullable=True)

    last_watered = Column(DateTime, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


    user = relationship("User", back_populates="plants")