from app.extensions import db
from app.forms import SettingsForm
from app.models import User, EmailTemplate
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

settings_bp = Blueprint("settings", __name__)

@settings_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    user_id = current_user.id
    form = SettingsForm()

    if request.method == "POST" and form.validate_on_submit():
        try:
            user = User.query.get(user_id)
            user.reminder_activate = form.reminder_activate.data
            user.reminder_timezone = form.reminder_timezone.data
            user.reminder_offset = int(form.reminder_offset.data)
            user.reminder_hour = int(form.reminder_hour.data)

            template = EmailTemplate.query.filter_by(user_id=user_id).first()
            if template:
                template.template_subject = form.email_subject.data.strip()
                template.template_body = form.email_body.data.strip()
            else:
                db.session.add(EmailTemplate(
                    user_id=user_id,
                    template_subject=form.email_subject.data.strip(),
                    template_body=form.email_body.data.strip()
                ))

            db.session.commit()
            return jsonify({"status": "success"}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 400

    elif request.method == "GET":
        user = User.query.get(user_id)
        template = EmailTemplate.query.filter_by(user_id=user_id).first()

        return jsonify({
            "reminder_activate": user.reminder_activate,
            "reminder_timezone": user.reminder_timezone,
            "reminder_offset": str(user.reminder_offset),
            "reminder_hour": str(user.reminder_hour),
            "email_subject": template.template_subject if template else "",
            "email_body": template.template_body if template else ""
        }), 200

    return jsonify({"status": "error", "message": "Invalid request"}), 400