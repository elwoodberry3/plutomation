# 'MAIN' - Bootstraps the FastAPI application and includes routers.
# Last updated on 12.14.2024

import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.routers import job_search, workflow_tracking
import logging
import time

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

app = FastAPI(debug=DEBUG_MODE)

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware for logging and performance metrics
class PerformanceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"{request.method} {request.url} - {response.status_code} - {process_time:.2f}s")
        return response

app.add_middleware(PerformanceMiddleware)

@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        logger.exception("Unhandled exception")
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})

# Include routers
app.include_router(job_search.router, prefix="/job_search", tags=["Job Search"])
app.include_router(workflow_tracking.router, prefix="/workflow", tags=["Workflow"])

@app.get("/")
async def root():
    return {"message": "Plutomation Employment Utility API"}
