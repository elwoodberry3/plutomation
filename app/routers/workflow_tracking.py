# 'WORKFLOW TRACKING' - Implements endpoints to update workflow stages.
# Last updated on 12.14.2024

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import WorkflowTracking
from app.schemas import WorkflowUpdate
import logging

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.put("/workflow/{workflow_id}")
async def update_workflow(
    workflow_id: int, update: WorkflowUpdate, db: AsyncSession = Depends(get_db)
):
    try:
        workflow = await db.get(WorkflowTracking, workflow_id)
        if not workflow:
            logger.error(f"Workflow with ID {workflow_id} not found.")
            raise HTTPException(status_code=404, detail="Workflow not found")

        workflow.stage = update.stage
        workflow.notes = update.notes
        workflow.completed = update.completed
        await db.commit()

        logger.info(f"Workflow {workflow_id} updated successfully.")
        return {"message": "Workflow updated successfully"}
    except Exception as e:
        logger.exception(f"Error updating workflow {workflow_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
