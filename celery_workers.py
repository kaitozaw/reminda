from app import create_app
from app.extensions import celery

flask_app = create_app()

with flask_app.app_context():
    import app.jobs.reminders
    import app.jobs.scheduler