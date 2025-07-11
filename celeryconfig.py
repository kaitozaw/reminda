from celery.schedules import crontab

beat_schedule = {
    "run-hourly-reminder": {
        "task": "jobs.scheduler.run_hourly_reminder_dispatch",
        "schedule": crontab(minute=0),
    },
}

timezone = "Australia/Brisbane"