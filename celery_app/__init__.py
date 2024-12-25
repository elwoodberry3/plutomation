# CELERY 'INIT' - Sets up the Celery instance with Redis as the broker and backend.
# Last updated on 12.14.2024

import os
from celery import Celery

# Configure Celery instance with environment variables
celery_app = Celery(
    "plutomation",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_BACKEND_URL", "redis://localhost:6379/0")
)

# Update Celery configuration
celery_app.conf.update(
    task_serializer="json",  # Serialize tasks in JSON format for readability
    result_serializer="json",  # Serialize results in JSON format for consistency
    accept_content=["json"],  # Restrict accepted content types to JSON for security
    timezone=os.getenv("CELERY_TIMEZONE", "UTC"),  # Set timezone, defaulting to UTC
    enable_utc=True,  # Ensure UTC is enabled for consistency across deployments
)

# Add comments to clarify usage of environment variables
# CELERY_BROKER_URL: URL for the message broker (e.g., Redis, RabbitMQ).
# CELERY_BACKEND_URL: URL for the result backend (e.g., Redis, database).
# CELERY_TIMEZONE: Timezone for task scheduling and timestamps.
