# 'MODELS' - Defines database models for job applications and workflow tracking.
# Last updated on 12.14.2024

from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String, index=True)
    company_name = Column(String)
    application_status = Column(String, default="Pending")
    applied_at = Column(DateTime, default=func.now())

class WorkflowTracking(Base):
    __tablename__ = "workflow_tracking"

    id = Column(Integer, primary_key=True, index=True)
    stage = Column(String)
    notes = Column(String)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
