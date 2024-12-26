# 'WORKFLOW TRACKING' - Implements endpoints to update workflow stages.
# Last updated on 12.26.2024

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import WorkflowTracking
from app.schemas import WorkflowUpdate
import logging

logger = logging.getLogger("workflow_tracking")
router = APIRouter()

@router.put("/workflow/{workflow_id}")
async def update_workflow(
    workflow_id: int, update: WorkflowUpdate, db: AsyncSession = Depends(get_db)
):
    """
    Update the stage, notes, and completion status of a workflow entry.
    """
    try:
        workflow = await db.get(WorkflowTracking, workflow_id)
        if not workflow:
            logger.error(f"Workflow {workflow_id} not found.")
            raise HTTPException(status_code=404, detail="Workflow not found")

        workflow.stage = update.stage
        workflow.notes = update.notes
        workflow.completed = update.completed
        await db.commit()
        return {"message": "Workflow updated successfully"}
    except Exception as e:
        logger.exception("Error updating workflow")
        raise HTTPException(status_code=500, detail="Internal server error")
