from fastapi import FastAPI
from app.routers import job_search, workflow_tracking

app = FastAPI()

app.include_router(job_search.router, prefix="/job_search", tags=["Job Search"])
app.include_router(workflow_tracking.router, prefix="/workflow", tags=["Workflow"])

@app.get("/")
async def root():
    return {"message": "Plutomation Employment Utility API"}