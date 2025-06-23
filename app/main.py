import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.router import router

logging.basicConfig(level=settings.log_level)

app = FastAPI(
    title="AI Compliance Tracker API",
    version="2.0.0",
    description="Real-time compliance metrics & AI‑driven insights"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.frontend_url_list,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "healthy"}