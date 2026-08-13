import os
import fastf1
from fastapi import FastAPI

from app.database import engine, Base
from app.routers import races, drivers, favorites

# Create SQL database tables automatically on application startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="F1 Tracker API",
    description="Full-stack F1 Dashboard with FastF1 & SQLite Database",
    version="0.4.0"
)

# Enable FastF1 Cache
CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", ".fastf1_cache")
os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(CACHE_DIR)

# Register Routers
app.include_router(races.router)
app.include_router(drivers.router)
app.include_router(favorites.router)

@app.get("/")
def root():
    return {"status": "online", "database": "connected (SQLite)"}