import fastf1
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.schemas.f1 import DriverResultSchema
router = APIRouter(
    prefix="/drivers",
    tags=["Drivers & Standings"]
)

@router.get("/{year}/{gp}", response_model=List[DriverResultSchema])
def get_driver_results(
    year: int,
    gp: str,
    team: Optional[str] = Query(None, description="Filter drivers by team name (e.g., 'Ferrari', 'Red Bull')")
):
    try:
        session = fastf1.get_session(year, gp, 'R')
        session.load(telemetry=False, weather=False)
        
        results = session.results[['DriverNumber', 'BroadcastName', 'TeamName', 'Position', 'Points']]
        records = results.to_dict(orient="records")
        
        if team:
            records = [d for d in records if team.lower() in d['TeamName'].lower()]
            
        return records
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch session: {str(e)}")

from app.schemas.f1 import DriverResultSchema, FastestLapSchema, DriverComparisonSchema

# Existing routes remain above...

@router.get("/{year}/{gp}/fastest-lap", response_model=FastestLapSchema)
def get_fastest_lap(year: int, gp: str, driver: str):
    """
    Fetch the fastest lap details for a specific driver in a Grand Prix.
    Example: /drivers/2024/Monaco/fastest-lap?driver=LEC
    """
    try:
        session = fastf1.get_session(year, gp, 'R')
        session.load(telemetry=False, weather=False)
        
        # Filter laps by driver abbreviation (e.g., 'VER', 'HAM', 'LEC')
        driver_laps = session.laps.pick_driver(driver.upper())
        if driver_laps.empty:
            raise HTTPException(status_code=4404, detail=f"No laps found for driver '{driver}'")
            
        fastest_lap = driver_laps.pick_fastest()
        
        return {
            "Driver": fastest_lap['Driver'],
            "LapTimeSeconds": fastest_lap['LapTime'].total_seconds(),
            "LapNumber": int(fastest_lap['LapNumber']),
            "Compound": str(fastest_lap['Compound'])
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{year}/{gp}/compare", response_model=DriverComparisonSchema)
def compare_drivers(year: int, gp: str, driver1: str, driver2: str):
    """
    Head-to-head comparison of fastest laps between two drivers.
    Example: /drivers/2024/Monaco/compare?driver1=VER&driver2=NOR
    """
    try:
        session = fastf1.get_session(year, gp, 'R')
        session.load(telemetry=False, weather=False)
        
        lap1 = session.laps.pick_driver(driver1.upper()).pick_fastest()
        lap2 = session.laps.pick_driver(driver2.upper()).pick_fastest()
        
        t1 = lap1['LapTime'].total_seconds()
        t2 = lap2['LapTime'].total_seconds()
        
        d1_data = {
            "Driver": lap1['Driver'],
            "LapTimeSeconds": t1,
            "LapNumber": int(lap1['LapNumber']),
            "Compound": str(lap1['Compound'])
        }
        
        d2_data = {
            "Driver": lap2['Driver'],
            "LapTimeSeconds": t2,
            "LapNumber": int(lap2['LapNumber']),
            "Compound": str(lap2['Compound'])
        }
        
        return {
            "event": session.event['EventName'],
            "year": year,
            "driver_1": d1_data,
            "driver_2": d2_data,
            "delta_seconds": round(abs(t1 - t2), 3)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Comparison failed: {str(e)}")