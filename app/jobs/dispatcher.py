def dispatch_reminders():
    from app.models import User, ReminderLog
    from app.jobs.reminder import reminder_email
    from datetime import datetime, timedelta
    import pytz

    now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
    users = User.query.filter_by(reminder_activate=True).all()
    for user in users:
        try:
            tz = pytz.timezone(user.reminder_timezone)
        except Exception:
            continue

        now_local = now_utc.astimezone(tz)
        if now_local.hour != user.reminder_hour:
            continue

        if user.reminder_offset not in [0, 1]:
            continue

        target_date = now_local.date()
        if user.reminder_offset == 1:
            target_date += timedelta(days=1)

        for event in user.events:
            event_date = event.start_time.astimezone(tz).date()
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