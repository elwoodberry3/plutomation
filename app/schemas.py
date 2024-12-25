# 'SCHEMAS' - Defines pydantic models for input and response validation.
# Last updated on 12.14.2024

from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class ApplicationStatus(str, Enum):
    PENDING = "Pending"
    APPLIED = "Applied"
    REJECTED = "Rejected"
    ACCEPTED = "Accepted"

class JobApplicationCreate(BaseModel):
    job_title: str = Field(..., min_length=1, max_length=100, description="Title of the job being applied for")
    company_name: str = Field(..., min_length=1, max_length=100, description="Name of the company")

class JobApplicationResponse(JobApplicationCreate):
    id: int
    application_status: ApplicationStatus
    applied_at: datetime

    class Config:
        orm_mode = True

class WorkflowUpdate(BaseModel):
    stage: str = Field(..., min_length=1, max_length=50, description="Current stage of the workflow")
    notes: str = Field(..., min_length=0, max_length=500, description="Optional notes for the workflow")
    completed: bool = Field(..., description="Whether the workflow is completed")
