from app import create_app
from app.extensions import db
from app.models import User, EmailTemplate
from datetime import datetime
import pytz

def create_test_user_and_template():
    AEST = pytz.timezone("Australia/Brisbane")
    now = datetime.now(AEST).replace(minute=0, second=0, microsecond=0)

    user = User(
        email="kaitozaw@gmail.com",
        reminder_offset=0,
        reminder_hour=now.hour
    )
    user.set_password("password")
    db.session.add(user)
    db.session.flush()

    template = EmailTemplate(
        user_id=user.id,
        template_subject="Reminder: {name}'s Cleaning Appointment",
        template_body="Hi {name}, please be ready at {event_time} at {location}."
    )
    db.session.add(template)

    db.session.commit()

    print("✅ Done! Test user & template created successfully.")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        create_test_user_and_template()