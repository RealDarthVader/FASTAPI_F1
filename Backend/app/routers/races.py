import fastf1
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.schemas.f1 import RaceEventSchema

router = APIRouter(
    prefix="/races",
    tags=["Races & Schedules"]
)

@router.get("/{year}", response_model=List[RaceEventSchema])
def get_schedule(
    year: int, 
    country: Optional[str] = Query(None, description="Filter races by country name (e.g., 'Monaco')")
):
   
    try:
        schedule = fastf1.get_event_schedule(year)
        cleaned = schedule[['RoundNumber', 'EventName', 'Country', 'Location', 'EventDate']].dropna(subset=['RoundNumber'])
        cleaned['EventDate'] = cleaned['EventDate'].astype(str)
        
        records = cleaned.to_dict(orient="records")
        

        if country:
            records = [r for r in records if country.lower() in r['Country'].lower()]
            
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))