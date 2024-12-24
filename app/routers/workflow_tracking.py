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