import os
import tempfile
import fastf1
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.database import engine, Base
from app.routers import races, drivers, favorites, search

# Initialize SQLite tables
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning on DB init: {e}")

app = FastAPI(
    title="F1 Tracker API",
    description="Full-stack F1 Dashboard with FastF1, SQLite Database, & Search",
    version="0.5.0"
)

# CORS Setup
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://fastapi-f1.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# FastF1 Cache Setup (Writable /tmp directory for Serverless)
CACHE_DIR = os.path.join(tempfile.gettempdir(), ".fastf1_cache")
os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(CACHE_DIR)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "InternalServerError", "message": str(exc), "path": str(request.url)}
    )

# Include Routers
app.include_router(races.router)
app.include_router(drivers.router)
app.include_router(favorites.router)
app.include_router(search.router)

@app.get("/")
def root():
    return {"status": "online", "version": "0.5.0", "cors": "enabled"}