# 'INIT' - Initializes the routers directory as a Python package and provides imports for all routers.
# Last updated on 12.14.2024

from .job_search import router as job_search_router
from .workflow_tracking import router as workflow_tracking_router

__all__ = [
    "job_search_router",
    "workflow_tracking_router"
]

__version__ = "1.1.0"
__author__ = "Plutomation Team"