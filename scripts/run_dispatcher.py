from app import create_app
from app.jobs.dispatcher import dispatch_reminders

app = create_app()

with app.app_context():
    dispatch_reminders()