import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import yaml

from src.backend.routes import ingest, generate, export, feedback
from src.backend.utils.logger import setup_logger

# Load config
with open("config/settings.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# Setup logger
setup_logger(config["logging"])

# Initialize FastAPI app
app = FastAPI(
    title="Camera TestGen Backend",
    description="API for generating BDD test cases from UI screenshots",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Set config in app state
app.state.config = config

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config["backend"]["cors_allowed_origins"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ingest.router, prefix=config["backend"]["api_prefix"])
app.include_router(generate.router, prefix=config["backend"]["api_prefix"])
app.include_router(export.router, prefix=config["backend"]["api_prefix"])
app.include_router(feedback.router, prefix=config["backend"]["api_prefix"])

@app.get("/")
def root():
    return {"message": "Camera TestGen Backend is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.backend.main:app",
        host=config["backend"]["host"],
        port=config["backend"]["port"],
        reload=config["backend"]["reload"]
    )