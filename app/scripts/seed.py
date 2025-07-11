from app.extensions import db
from app.models import User, Customer, GoogleEvent, EventAssignment, EmailTemplate, ReminderLog, ReminderStatus
from datetime import datetime, timedelta
import pytz

def create_test_user_and_events():
    AEST = pytz.timezone("Australia/Brisbane")
    now = datetime.now(AEST).replace(minute=0, second=0, microsecond=0)

    user = User(
        email="kaitozaw@gmail.com",
        reminder_hour=now.hour,
        reminder_offset=0
    )
    user.set_password("password")
    db.session.add(user)
    db.session.flush()

    customer = Customer(
        user_id=user.id,
        first_name="Kaito",
        last_name="Ozawa",
        email="kaito.ozawa@connect.qut.edu.au",
        tel="+61412345678",
        location="Brisbane",
        description="Test Customer"
    )
    db.session.add(customer)
    db.session.flush()

    event1 = GoogleEvent(
        user_id=user.id,
        google_event_id="test-event-1",
        calendar_id="test-calendar",
        title="Cleaning Session 1",
        start_time=now + timedelta(hours=2),
        end_time=now + timedelta(hours=3),
        location="Brisbane",
        description="Test Event 1"
    )
    db.session.add(event1)

    event2 = GoogleEvent(
        user_id=user.id,
        google_event_id="test-event-2",
        calendar_id="test-calendar",
        title="Cleaning Session 2",
        start_time=now + timedelta(days=1, hours=2),
        end_time=now + timedelta(days=1, hours=3),
        location="Brisbane",
        description="Test Event 2"
    )
    db.session.add(event2)

    event3 = GoogleEvent(
        user_id=user.id,
        google_event_id="test-event-3",
        calendar_id="test-calendar",
        title="Cleaning Session 3",
        start_time=now + timedelta(days=2, hours=2),
        end_time=now + timedelta(days=2, hours=3),
        location="Brisbane",
        description="Test Event 3"
    )
    db.session.add(event3)
    db.session.flush()

    db.session.add_all([
        EventAssignment(customer_id=customer.id, event_id=event1.id),
        EventAssignment(customer_id=customer.id, event_id=event2.id),
        EventAssignment(customer_id=customer.id, event_id=event3.id),
    ])

    template = EmailTemplate(
        user_id=user.id,
        template_subject="Reminder: {name}'s Cleaning Appointment",
        template_body="Hi {name}, please be ready at {event_time} at {location}."
    )
    db.session.add(template)

    log1 = ReminderLog(
        user_id=user.id,
        customer_id=customer.id,
        event_id=event1.id,
        status=ReminderStatus.SENT,
        email_subject="Reminder: Cleaning Session 1",
        email_body="Hi Kaito, please be ready at Brisbane for Event 1."
    )

    log2 = ReminderLog(
        user_id=user.id,
        customer_id=customer.id,
        event_id=event2.id,
        status=ReminderStatus.FAILED,
        email_subject="Reminder: Cleaning Session 2",
        email_body="Hi Kaito, please be ready at Brisbane for Event 2."
    )

    db.session.add_all([log1, log2])
    db.session.commit()

    print("✅ Done! Test user, customer, 3 events, and 2 reminder logs created successfully.")