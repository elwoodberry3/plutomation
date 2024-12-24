# Framework
Setting up a FastAPI backend for Plutomation’s employment utility application. 
The application automates job applications, recruiter responses, and workflow tracking. 

- Configure FastAPI
- Connect a database
- Define endpoints for inter-agent communication.

---

## Step 1: Install Required Packages

Begin by setting up a virtual environment and installing necessary packages:

```bash
# Create and activate a virtual environment
python3 -m venv env
source env/bin/activate

# Install FastAPI, Uvicorn, and additional dependencies
pip install fastapi uvicorn[standard] sqlalchemy asyncpg pydantic python-multipart
```

---

## Step 2: Project Structure

Organize your project with the following structure:

```
plutomation_app/
|-- app/
|   |-- __init__.py
|   |-- main.py
|   |-- models.py
|   |-- schemas.py
|   |-- database.py
|   |-- routers/
|       |-- __init__.py
|       |-- job_search.py
|       |-- recruiter_response.py
|       |-- workflow_tracking.py
|-- env/
|-- requirements.txt
```

---

## Step 3: Database Configuration

### File: `app/database.py`

Set up a connection to a PostgreSQL database using SQLAlchemy.

```python
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

Replace `user`, `password`, and `plutomation_db` with your database credentials.

---

## Step 4: Define Models and Schemas

### File: `app/models.py`

Define database models for job applications and workflow tracking.

```python
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

### File: `app/schemas.py`

Define Pydantic schemas for request validation.

```python
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

---

## Step 5: Create API Endpoints

### File: `app/routers/job_search.py`

Create endpoints for job search and application.

```python
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
```

### File: `app/routers/workflow_tracking.py`

Create endpoints for tracking workflow stages.

```python
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

---

## Step 6: Main Application File

### File: `app/main.py`

Set up the FastAPI instance and include routers.

```python
from fastapi import FastAPI
from app.routers import job_search, workflow_tracking

app = FastAPI()

app.include_router(job_search.router, prefix="/job_search", tags=["Job Search"])
app.include_router(workflow_tracking.router, prefix="/workflow", tags=["Workflow"])

@app.get("/")
async def root():
    return {"message": "Plutomation Employment Utility API"}
```

---

## Step 7: Run the Application

Run the FastAPI application with Uvicorn.

```bash
uvicorn app.main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

---

## Conclusion

With FastAPI, you’ve created a scalable and efficient backend for Plutomation’s employment utility application. This setup allows seamless API interactions between agents and ensures extensibility for future features. Happy coding!
