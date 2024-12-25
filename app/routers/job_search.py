
# 'JOB SEARCH' - defines endpoints for job application submission and triggers asynchronous job application tasks using Celery.
# Last updated on 12.14.2024

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import JobApplication
from app.schemas import JobApplicationCreate, JobApplicationResponse
from celery_app import celery_app

router = APIRouter()

@router.post("/jobs/", response_model=JobApplicationResponse)
async def apply_to_job(
    job: JobApplicationCreate, db: AsyncSession = Depends(get_db)
):
    new_job = JobApplication(
        job_title=job.job_title, company_name=job.company_name, application_status="Applied"
    )
    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)
    return new_job

@celery_app.task
def apply_to_job_task(job_details: dict):
    # Simulate applying to a job
    print(f"Applying to job: {job_details['job_title']} at {job_details['company_name']}")
    return {"status": "success", "job_title": job_details["job_title"]}

@router.post("/jobs/apply")
async def trigger_job_application(job_details: JobApplicationCreate):
    try:
        task = apply_to_job_task.delay(job_details.dict())
        return {"task_id": task.id, "status": "Job application task created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to trigger job application: {str(e)}")
