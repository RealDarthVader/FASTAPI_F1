from pydantic import BaseModel, Field
from typing import Optional

class DriverResultSchema(BaseModel):
    driver_number: str = Field(..., alias="DriverNumber")
    broadcast_name: str = Field(..., alias="BroadcastName")
    team_name: str = Field(..., alias="TeamName")
    position: Optional[float] = Field(None, alias="Position")
    points: float = Field(0.0, alias="Points")

    class Config:
        populate_by_name = True

class RaceEventSchema(BaseModel):
    round_number: int = Field(..., alias="RoundNumber")
    event_name: str = Field(..., alias="EventName")
    country: str = Field(..., alias="Country")
    location: str = Field(..., alias="Location")
    event_date: str = Field(..., alias="EventDate")

    class Config:
        populate_by_name = True

class FastestLapSchema(BaseModel):
    driver: str = Field(..., alias="Driver")
    lap_time_seconds: float = Field(..., alias="LapTimeSeconds")
    lap_number: int = Field(..., alias="LapNumber")
    compound: str = Field(..., alias="Compound")

    class Config:
        populate_by_name = True

class DriverComparisonSchema(BaseModel):
    event: str
    year: int
    driver_1: FastestLapSchema
    driver_2: FastestLapSchema
    delta_seconds: float