from typing import List, Optional
import fastf1
from fastapi import APIRouter, HTTPException, Query
import pandas as pd
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
    """
    Fetch driver race results for a specific Grand Prix.
    Supports both modern (2018+) and historic (1950-2017) sessions.
    """
    try:
        session = fastf1.get_session(year, gp, 'R')
        session.load(telemetry=False, weather=False)
        
        results = session.results.copy()
        
        # Determine the best available driver name column across eras
        if 'BroadcastName' in results.columns and results['BroadcastName'].dropna().any():
            driver_col = results['BroadcastName']
        elif 'FullName' in results.columns and results['FullName'].dropna().any():
            driver_col = results['FullName']
        elif 'GivenName' in results.columns and 'FamilyName' in results.columns:
            driver_col = results['GivenName'].fillna('') + ' ' + results['FamilyName'].fillna('')
        elif 'Abbreviation' in results.columns:
            driver_col = results['Abbreviation']
        else:
            driver_col = results['DriverNumber']
            
        results['BroadcastName'] = driver_col.fillna('Unknown Driver')
        
        # Ensure fallback for required columns
        for col in ['DriverNumber', 'BroadcastName', 'TeamName', 'Position', 'Points']:
            if col not in results.columns:
                results[col] = None

        cleaned_results = results[['DriverNumber', 'BroadcastName', 'TeamName', 'Position', 'Points']]
        records = cleaned_results.to_dict(orient="records")
        
        if team:
            records = [d for d in records if d.get('TeamName') and team.lower() in str(d['TeamName']).lower()]
            
        return records
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch session: {str(e)}")