
# 'JOB SEARCH' - Implements job application-related endpoints. Defines endpoints for job application submission and triggers asynchronous job application tasks using Celery.
# Last updated on 12.26.2024

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import JobApplication
from app.schemas import JobApplicationCreate, JobApplicationResponse
from celery_app import celery_app
import logging

logger = logging.getLogger("job_search")
router = APIRouter()

@router.post("/jobs/", response_model=JobApplicationResponse)
async def apply_to_job(
    job: JobApplicationCreate, db: AsyncSession = Depends(get_db)
):
    """
    Endpoint to create a job application entry in the database.
    """
    try:
        new_job = JobApplication(
            job_title=job.job_title, company_name=job.company_name, application_status="Applied"
        )
        db.add(new_job)
        await db.commit()
        await db.refresh(new_job)
        return new_job
    except Exception as e:
        logger.exception("Error applying to job")
        raise HTTPException(status_code=500, detail=f"Failed to apply: {str(e)}")

@celery_app.task
def apply_to_job_task(job_details: dict):
    """
    Celery task to asynchronously handle job applications.
    """
    logger.info(f"Processing job application: {job_details}")
    return {"status": "success", "job_title": job_details["job_title"]}

@router.post("/jobs/apply")
async def trigger_job_application(job_details: JobApplicationCreate):
    """
    Trigger an asynchronous task for a job application.
    """
    try:
        task = apply_to_job_task.delay(job_details.dict())
        return {"task_id": task.id, "status": "Job application task created"}
    except Exception as e:
        logger.exception("Error triggering job application task")
        raise HTTPException(status_code=500, detail=f"Failed to trigger job application: {str(e)}")
