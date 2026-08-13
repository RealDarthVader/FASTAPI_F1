from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.f1 import FavoriteDriverModel
from app.schemas.f1 import FavoriteDriverCreateSchema, FavoriteDriverResponseSchema

router = APIRouter(
    prefix="/favorites",
    tags=["User Favorites (SQL Database)"]
)

@router.post("/", response_model=FavoriteDriverResponseSchema, status_code=status.HTTP_201_CREATED)
def add_favorite(fav: FavoriteDriverCreateSchema, db: Session = Depends(get_db)):
    """
    Save a driver to local SQLite database favorites list.
    """
    existing = db.query(FavoriteDriverModel).filter(FavoriteDriverModel.driver_code == fav.driver_code.upper()).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Driver '{fav.driver_code}' is already in your favorites.")

    new_fav = FavoriteDriverModel(
        driver_code=fav.driver_code.upper(),
        driver_name=fav.driver_name,
        team_name=fav.team_name,
        user_notes=fav.user_notes
    )
    db.add(new_fav)
    db.commit()
    db.refresh(new_fav)
    return new_fav

@router.get("/", response_model=List[FavoriteDriverResponseSchema])
def get_favorites(db: Session = Depends(get_db)):
    """
    Fetch all saved favorite drivers from SQLite.
    """
    return db.query(FavoriteDriverModel).all()

@router.delete("/{driver_code}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite(driver_code: str, db: Session = Depends(get_db)):
    """
    Remove a driver from favorites by driver code (e.g., 'VER').
    """
    fav = db.query(FavoriteDriverModel).filter(FavoriteDriverModel.driver_code == driver_code.upper()).first()
    if not fav:
        raise HTTPException(status_code=404, detail=f"Driver '{driver_code}' not found in favorites.")
    
    db.delete(fav)
    db.commit()
    return None