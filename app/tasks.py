# 'TASKS' - Defines Celery tasks for job application processing and recruiter email notifications.
# Last updated on 12.14.2024

from celery_app import celery_app
import logging

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_job_application(job_details):
    """Helper function to process job applications."""
    if not isinstance(job_details, dict) or 'job_title' not in job_details or 'company_name' not in job_details:
        raise ValueError("Invalid job details provided")

    logger.info(f"Processing job application for {job_details['job_title']} at {job_details['company_name']}")
    return {"status": "success", "job_title": job_details["job_title"]}

def process_recruiter_email(email_data):
    """Helper function to send recruiter emails."""
    if not isinstance(email_data, dict) or 'email' not in email_data:
        raise ValueError("Invalid email data provided")

    logger.info(f"Sending email to recruiter: {email_data['email']}")
    return {"status": "sent", "email": email_data["email"]}

@celery_app.task
def apply_to_job(job_details):
    try:
        result = process_job_application(job_details)
        return result
    except Exception as e:
        logger.exception("Failed to apply to job")
        return {"status": "error", "message": str(e)}

@celery_app.task
def send_recruiter_email(email_data):
    try:
        result = process_recruiter_email(email_data)
        return result
    except Exception as e:
        logger.exception("Failed to send recruiter email")
        return {"status": "error", "message": str(e)}
