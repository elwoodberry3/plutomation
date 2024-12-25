# Application Manifest
This is the application manifest for the Plutomation utility application.

Project Structure
```bash
plutomation_app/
|-- _assets/
|   |-- app-manifest.md
|   |-- imgs/
|   |-- plutomation-github-billboard.jpg
|-- app/
|   |-- __init__.py
|   |-- main.py
|   |-- tasks.py
|   |-- models.py
|   |-- schemas.py
|   |-- database.py
|   |-- routers/
|       |-- __init__.py
|       |-- job_search.py
|       |-- recruiter_response.py
|       |-- workflow_tracking.py
|-- celery_app/
|   |-- __init__.py
|-- env/
|   |-- bin/
|   |-- include/
|   |-- lib/
|   |-- pyvenv.cfg
|-- README.md
```

## Assets ('_assets')
This directory serves as a repository for non-application files, such as static images and documentation like the app-manifest.md. This separation ensures the core application remains lightweight and focused.

## Application ('app/')
Contains the main business logic, APIs, and database interactions. It is the backbone of the utility, designed with FastAPI.

## Routers ('app/routers/')
Houses FastAPI routers for modular API endpoint definitions. This directory promotes separation of concerns and ease of maintenance.

### Initialize ('app/routers/__init__.py')
Blank file to initialize the directory as a Python package. Consider adding imports for routers or metadata for easier integration.
```bash 
# File is blank 
```  

### Job Search ('app/routers/job_search.py')  
Defines endpoints for job application submission and triggers asynchronous job application tasks using Celery.  
```bash 
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


@router.post("/jobs/apply")
async def trigger_job_application(job_details: dict):
    task = apply_to_job.delay(job_details)
    return {"task_id": task.id, "status": "Job application task created"}
```  

### Recruiter Response ('app/routers/recruiter_response.py')
[write a 100 character description for this file and its responsibilities]
```bash 
# File is blank 
```  

### Workflow Tracking ('app/routers/workflow_tracking.py')
[write a 100 character description for this file and its responsibilities]
```bash 
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import WorkflowTracking
from app.schemas import WorkflowUpdate

router = APIRouter()

@router.put("/workflow/{workflow_id}")
async def update_workflow(
    workflow_id: int, update: WorkflowUpdate, db: AsyncSession = Depends(get_db)
):
    workflow = await db.get(WorkflowTracking, workflow_id)
    if workflow:
        workflow.stage = update.stage
        workflow.notes = update.notes
        workflow.completed = update.completed
        await db.commit()
        return {"message": "Workflow updated successfully"}
    return {"error": "Workflow not found"}
```  

### Initialize ('app/__init__.py')
[write a 100 character description for this file and its responsibilities]
```bash 
# File is blank 
```  
  
### Main ('app/main.py')
Bootstraps the FastAPI application and includes routers.
```bash
from fastapi import FastAPI
from app.routers import job_search, workflow_tracking

app = FastAPI()

app.include_router(job_search.router, prefix="/job_search", tags=["Job Search"])
app.include_router(workflow_tracking.router, prefix="/workflow", tags=["Workflow"])

@app.get("/")
async def root():
    return {"message": "Plutomation Employment Utility API"}  
```  
  
### Tasks ('app/tasks.py')
Defines Celery tasks for job application processing and recruiter email notifications.
```bash 
from celery_app import celery_app

@celery_app.task
def apply_to_job(job_details):
    # Simulate applying to a job
    print(f"Applying to job: {job_details['job_title']} at {job_details['company_name']}")
    return {"status": "success", "job_title": job_details["job_title"]}

@celery_app.task
def send_recruiter_email(email_data):
    # Simulate sending an email to a recruiter
    print(f"Sending email to recruiter: {email_data['email']}")
    return {"status": "sent", "email": email_data["email"]} 
```  
  
### Models ('app/models.py')
Defines database models for job applications and workflow tracking.
```bash 
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String, index=True)
    company_name = Column(String)
    application_status = Column(String, default="Pending")
    applied_at = Column(DateTime)

class WorkflowTracking(Base):
    __tablename__ = "workflow_tracking"

    id = Column(Integer, primary_key=True, index=True)
    stage = Column(String)
    notes = Column(String)
    completed = Column(Boolean, default=False) 
```  
  
### Schemas ('app/schemas.py')
Defines pydantic models for input and response validation.  
```bash  
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
```  
  
### Database ('app/database.py')
Handles database session management and engine creation.
```bash 
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/plutomation_db"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with async_session() as session:
        yield session 
```  
  
## Celery App ('celery_app/')
[write a 200 character description for this directory]
  
### Initialize ('celery_app/__init__.py')
Sets up the Celery instance with Redis as the broker and backend.
```bash 
from celery import Celery

# Configure Celery instance
celery_app = Celery(
    "plutomation",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
) 
```  
  
## Environment ('env/')
Contains the Python virtual environment for dependency management.
  
### Bin ('env/bin/')
Houses executable scripts for the virtual environment.
  
### Include ('env/include/')
Contains header files for Python packages.
  
### Library ('env/lib/')
Stores installed Python libraries.
  
### PYV ENV ('env/pyvenv.cfg')
Configuration file for the virtual environment.
```bash  
home = /opt/homebrew/opt/python@3.13/bin
include-system-site-packages = false
version = 3.13.0
executable = /opt/homebrew/Cellar/python@3.13/3.13.0_1/Frameworks/Python.framework/Versions/3.13/bin/python3.13
command = /opt/homebrew/opt/python@3.13/bin/python3.13 -m venv /Users/adbyrd/Documents/clients/elwood.berry/repos/plutomation/env
```  
  