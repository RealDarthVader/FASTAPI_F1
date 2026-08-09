import os
import fastf1
from fastapi import FastAPI
from app.routers import races, drivers

app = FastAPI(
    title="F1 Tracker API",
    description="Modular F1 Dashboard powered by FastF1 & Pydantic",
    version="0.2.0"
)

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", ".fastf1_cache")
os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(CACHE_DIR)

app.include_router(races.router)
app.include_router(drivers.router)

@app.get("/")
def root():
    return {"status": "online", "version": "0.2.0"}