from pydantic import BaseModel
from datetime import datetime

class JobApplicationCreate(BaseModel):
    job_title: str
    company_name: str

class JobApplicationResponse(JobApplicationCreate):
    id: int
    application_status: str
    applied_at: datetime

    class Config:
        orm_mode = True

class WorkflowUpdate(BaseModel):
    stage: str
    notes: str
    completed: bool