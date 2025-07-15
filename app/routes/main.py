from app.forms import SettingsForm
from app.models import ReminderLog, GoogleAccount
from datetime import datetime
from flask import Blueprint, render_template
from flask_login import login_required, current_user
import pytz

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
@login_required
def index():
    form = SettingsForm()

    google_account = GoogleAccount.query.filter_by(user_id=current_user.id).first()

    reminder_logs = ReminderLog.query.filter_by(user_id=current_user.id).order_by(ReminderLog.sent_at.desc()).all()
    reminder_tz = pytz.timezone(current_user.reminder_timezone or "UTC")
    reminder_logs_tz = []
    for reminder_log in reminder_logs:
        local_time = reminder_log.sent_at.replace(tzinfo=pytz.utc).astimezone(reminder_tz)
        reminder_logs_tz.append({
            "customer_name": f"{reminder_log.customer.first_name} {reminder_log.customer.last_name}",
            "event_title": reminder_log.event.title,
            "sent_at_local": local_time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": reminder_log.status
        })


    return render_template("index.html", form=form, google_account=google_account, reminder_logs_tz=reminder_logs_tz)