def dispatch_reminders():
    from app.models import User, ReminderLog
    from app.jobs.reminder import reminder_email
    from datetime import datetime, timedelta
    import os
    import pytz
    
    AEST = pytz.timezone("Australia/Brisbane")
    now_local = datetime.now(AEST)
    current_hour = now_local.hour
    print(f"[Scheduler] {now_local.strftime('%Y-%m-%d %H:%M')} AEST - Dispatching reminders for hour={current_hour}")
    print("DATABASE_URL from env:", os.environ.get("DATABASE_URL"))

    users = User.query.filter_by(reminder_hour=current_hour).all()
    for user in users:
        if user.reminder_offset not in [0, 1]:
            continue

        target_date = now_local.date()
        if user.reminder_offset == 1:
            target_date += timedelta(days=1)

        for event in user.events:
            event_date = event.start_time.astimezone(AEST).date()
            if event_date != target_date:
                continue

            for assignment in event.event_assignments:
                customer = assignment.customer

                exists = ReminderLog.query.filter_by(
                    customer_id=customer.id,
                    event_id=event.id
                ).first()

                if exists:
                    print(f"[Skipped] Already sent to customer={customer.id} for event={event.id}")
                    continue

                reminder_email(user.id, customer.id, event.id)
                print(f"[Enqueued] user={user.id}, customer={customer.id}, event={event.id}")