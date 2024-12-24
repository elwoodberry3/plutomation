from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import JobApplication
from app.schemas import JobApplicationCreate, JobApplicationResponse

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