from app.forms import SettingsForm
from app.models import ReminderLog, GoogleAccount
from flask import Blueprint, render_template
from flask_login import login_required, current_user

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
@login_required
def index():
    form = SettingsForm()

    reminder_logs = (
        ReminderLog.query
        .filter_by(user_id=current_user.id)
        .order_by(ReminderLog.sent_at.desc())
        .all()
    )

    google_account = GoogleAccount.query.filter_by(user_id=current_user.id).first()

    return render_template("index.html", form=form, reminder_logs=reminder_logs, google_account=google_account)