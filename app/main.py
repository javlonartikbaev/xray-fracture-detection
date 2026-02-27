import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.database import init_db
from app.routers import predictions, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    os.makedirs(settings.upload_dir, exist_ok=True)
    yield


app = FastAPI(
    title="X-Ray Fracture Detection API",
    description="AI-powered system for automated X-ray image analysis and bone fracture detection",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(users.router)
app.include_router(predictions.router)


@app.get("/")
async def root():
    return {"message": "X-Ray Fracture Detection API", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
