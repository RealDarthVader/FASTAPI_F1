import os
import fastf1
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.database import engine, Base
from app.routers import races, drivers, favorites, search

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="F1 Tracker API",
    description="Full-stack F1 Dashboard with FastF1, SQLite Database, & Search",
    version="0.5.0"
)

origins = [
    "http://localhost:3000",
    "http://localhost:5173",  
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", ".fastf1_cache")
os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(CACHE_DIR)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "InternalServerError", "message": str(exc), "path": str(request.url)}
    )

app.include_router(races.router)
app.include_router(drivers.router)
app.include_router(favorites.router)
app.include_router(search.router)

@app.get("/")
def root():
    return {"status": "online", "version": "0.5.0", "cors": "enabled"}