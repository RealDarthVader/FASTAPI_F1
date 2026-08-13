from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base

class FavoriteDriverModel(Base):
    __tablename__ = "favorite_drivers"

    id = Column(Integer, primary_key=True, index=True)
    driver_code = Column(String, nullable=False)
    driver_name = Column(String, nullable=False)
    team_name = Column(String, nullable=False)
    user_notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))