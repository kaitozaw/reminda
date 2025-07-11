from app.extensions import celery, db
from app.models import Customer, EmailTemplate, GoogleEvent, ReminderLog, ReminderStatus, User
from app.utils.gmail import send_email_via_gmail

@celery.task
def send_reminder_email(user_id, customer_id, event_id):
    from app import create_app
    app = create_app()
    with app.app_context():
        user = User.query.get(user_id)
        customer = Customer.query.get(customer_id)
        event = GoogleEvent.query.get(event_id)
        template = EmailTemplate.query.filter_by(user_id=user_id).first()

        if not (user and customer and event and template):
            return

        try:
            subject = template.template_subject.format(
                name=f"{customer.first_name} {customer.last_name}",
                location=event.location,
                event_time=event.start_time.strftime("%Y-%m-%d %H:%M")
            )
            body = template.template_body.format(
                name=f"{customer.first_name} {customer.last_name}",
                location=customer.location,
                event_time=event.start_time.strftime("%Y-%m-%d %H:%M")
            )

            status_code, message = send_email_via_gmail(
                user_id=user.id,
                to_email=customer.email,
                subject=subject,
                body=body
            )

            if status_code == 202:
                log_status = ReminderStatus.SENT
            else:
                log_status = ReminderStatus.FAILED

            db.session.merge(ReminderLog(
                customer_id=customer.id,
                event_id=event.id,
                user_id=user.id,
                status=log_status,
                email_subject=subject,
                email_body=body
            ))
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            db.session.merge(ReminderLog(
                customer_id=customer.id,
                event_id=event.id,
                status=ReminderStatus.FAILED,
                email_subject="(ERROR)",
                email_body=str(e)
            ))
            db.session.commit()