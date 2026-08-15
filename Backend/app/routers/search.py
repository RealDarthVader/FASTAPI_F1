import fastf1
from fastapi import APIRouter, HTTPException, Query
from app.schemas.f1 import SearchResultsSchema

router = APIRouter(
    prefix="/search",
    tags=["Global Search"]
)

@router.get("/", response_model=SearchResultsSchema)
def search_all(
    q: str = Query(..., min_length=2, description="Search term (driver name, team, country, or circuit)"),
    year: int = Query(2024, description="F1 Season year to search within")
):
    """
    Search across race events, circuits, drivers, and teams for a given season.
    """
    query_clean = q.strip().lower()
    matched_events = []
    matched_drivers = []

    try:
        schedule = fastf1.get_event_schedule(year)
        cleaned_sched = schedule[['RoundNumber', 'EventName', 'Country', 'Location', 'EventDate']].dropna(subset=['RoundNumber'])
        cleaned_sched['EventDate'] = cleaned_sched['EventDate'].astype(str)
        all_events = cleaned_sched.to_dict(orient="records")

        for event in all_events:
            if (query_clean in event['EventName'].lower() or 
                query_clean in event['Country'].lower() or 
                query_clean in event['Location'].lower()):
                matched_events.append(event)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying schedule: {str(e)}")

    try:
        session = fastf1.get_session(year, 1, 'R')
        session.load(telemetry=False, weather=False)
        
        results = session.results[['DriverNumber', 'BroadcastName', 'TeamName', 'Position', 'Points']]
        all_drivers = results.to_dict(orient="records")

        for d in all_drivers:
            if (query_clean in str(d['BroadcastName']).lower() or 
                query_clean in str(d['TeamName']).lower() or
                query_clean == str(d['DriverNumber'])):
                matched_drivers.append(d)
    except Exception:
        pass

    total = len(matched_events) + len(matched_drivers)

    return {
        "query": q,
        "year": year,
        "matching_events": matched_events,
        "matching_drivers": matched_drivers,
        "total_matches": total
    }